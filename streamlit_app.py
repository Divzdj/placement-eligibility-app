import streamlit as st
from src.db_manager import DatabaseManager

# Initialize DB manager
db = DatabaseManager()

# Helper function to load queries from .sql file
def load_sql_queries(filename):
    with open(filename, 'r') as file:
        sql_file = file.read()
    queries = [q.strip() for q in sql_file.split(';') if q.strip()]
    return queries

# Titles for insights
insight_titles = [
    "Average Problems Solved by Course Batch",
    "Placement Status Distribution",
    "Average Mock Interview Score by Enrollment Year",
    "Top 5 Students by Mock Interview Score",
    "Distribution of Average Soft Skills Score by Batch",
    "Placement Package Statistics by Course Batch",
    "Internships Completed vs Placement Readiness",
    "Average Programming Certifications by Placement Status",
    "Average Communication and Teamwork Scores by Graduation Year",
    "Interview Rounds Cleared vs Placement Status"
]

# Set page config
st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("Placement Eligibility Streamlit App")

# Sidebar mode switch
mode = st.sidebar.radio("Choose View", ["Eligible Students", "Data Preview", "Insights"])

# ---------------- ELIGIBLE STUDENTS ----------------
if mode == "Eligible Students":
    st.sidebar.header("Filter Criteria")

    problems_solved = st.sidebar.slider("Minimum Problems Solved", 0, 150, 50)
    soft_skill_score = st.sidebar.slider("Minimum Average Soft Skill Score", 0, 100, 70)
    mock_score = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 60)

    query = """
    SELECT s.student_id, s.name, s.email, s.course_batch, p.problems_solved,
           ss.communication, ss.teamwork, ss.presentation,
           pl.mock_interview_score, pl.placement_status
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
    JOIN SoftSkills ss ON s.student_id = ss.student_id
    JOIN Placements pl ON s.student_id = pl.student_id
    WHERE p.problems_solved >= ?
      AND (
          (ss.communication + ss.teamwork + ss.presentation + ss.leadership +
           ss.critical_thinking + ss.interpersonal_skills) / 6
      ) >= ?
      AND pl.mock_interview_score >= ?
    ORDER BY p.problems_solved DESC
    """

    df = db.fetch_dataframe(query, params=(problems_solved, soft_skill_score, mock_score))

    st.subheader("Eligible Students")
    st.write(f"Found {df.shape[0]} students matching the criteria.")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Results",
        data=df.to_csv(index=False),
        file_name="eligible_students.csv",
        mime="text/csv"
    )

# ---------------- DATA PREVIEW ----------------
elif mode == "Data Preview":
    st.subheader("Data Preview")
    table = st.selectbox("Select Table to Preview", ["Students", "Programming", "SoftSkills", "Placements"])
    preview_query = f"SELECT * FROM {table}"
    preview_df = db.fetch_dataframe(preview_query)
    st.dataframe(preview_df, use_container_width=True)

# ---------------- INSIGHTS ----------------
elif mode == "Insights":
    st.subheader("Placement Insights")

    queries = load_sql_queries("insights.sql")

    for idx, query in enumerate(queries):
        st.markdown(f"### {insight_titles[idx]}")

        try:
            df = db.fetch_dataframe(query)

            if df.empty:
                st.warning("No data available for this insight.")
                continue

            st.dataframe(df, use_container_width=True)

            # Visualizations for each insight
            if idx == 0:  # Avg Problems Solved per Batch
                st.bar_chart(df.set_index("course_batch")["avg_problems_solved"])

            elif idx == 1:  # Placement Status Distribution
                st.bar_chart(df.set_index("placement_status")["student_count"])

            elif idx == 2:  # Avg Mock Score by Enrollment Year
                st.line_chart(df.set_index("enrollment_year")["avg_mock_score"])

            elif idx == 3:  # Top 5 Students by Mock Score
                st.bar_chart(df.set_index("name")["mock_interview_score"])

            elif idx == 4:  # Avg Soft Skills by Batch
                st.line_chart(df.set_index("course_batch")["avg_soft_skills_score"])

            elif idx == 5:  # Placement Package Stats by Batch
                st.bar_chart(df.set_index("course_batch")["avg_package"])

            elif idx == 6:  # Internships vs Placement Readiness
                st.bar_chart(df.set_index("internships_completed")["placed_count"])

            elif idx == 7:  # Avg Certifications by Placement Status
                st.bar_chart(df.set_index("placement_status")["avg_certifications"])

            elif idx == 8:  # Comm & Teamwork by Graduation Year
                st.line_chart(df.set_index("graduation_year")[["avg_communication", "avg_teamwork"]])

            elif idx == 9:  # Interview Rounds vs Placement Status
                st.line_chart(df.set_index("interview_rounds_cleared")["placed_count"])

        except Exception as e:
            st.error(f"Error running insight {idx + 1}: {e}")
