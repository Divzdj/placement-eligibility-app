import streamlit as st
from src.db_manager import DatabaseManager
import pandas as pd

db = DatabaseManager("placement.db")


# -------------------- Page setup --------------------
st.set_page_config(page_title="Placement App", layout="wide")
st.title("My Placement Eligibility App (Beginner Version)")

# Sidebar options
option = st.sidebar.radio("Choose one option", ["Check Eligible Students", "See Table Data", "See Insights"])

# -------------------- Check Eligible Students --------------------
if option == "Check Eligible Students":
    st.sidebar.header("Set Your Filters")

    min_problems = st.sidebar.slider("Minimum Problems Solved", 0, 200, 30)
    min_softskills = st.sidebar.slider("Minimum Soft Skills Average", 0, 10, 6)
    min_mock = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 50)

    # Fetch combined data
    sql = """
        SELECT s.student_id, s.name, s.email, s.course_batch, 
               p.problems_solved, p.certifications_earned,
               ss.communication, ss.teamwork, ss.presentation, 
               ss.leadership, ss.critical_thinking, ss.interpersonal_skills,
               pl.mock_interview_score, pl.placement_status
        FROM Students s
        JOIN Programming p ON s.student_id = p.student_id
        JOIN SoftSkills ss ON s.student_id = ss.student_id
        JOIN Placements pl ON s.student_id = pl.student_id
    """
    df = db.fetch_dataframe(sql)

    # Calculate average soft skills
    soft_cols = ["communication", "teamwork", "presentation", "leadership", "critical_thinking", "interpersonal_skills"]
    df["avg_softskills"] = df[soft_cols].mean(axis=1)

    # Apply filters
    filtered = df[
        (df["problems_solved"] >= min_problems) &
        (df["avg_softskills"] >= min_softskills) &
        (df["mock_interview_score"] >= min_mock)
    ]

    st.subheader("Students who matched the filters")
    st.write("Number of students found:", filtered.shape[0])
    st.dataframe(filtered)

    st.download_button(
        "Download as CSV",
        data=filtered.to_csv(index=False).encode('utf-8'),
        file_name="eligible_students.csv",
        mime="text/csv"
    )

# -------------------- See Table Data --------------------
elif option == "See Table Data":
    st.subheader("See any Table")
    table_name = st.selectbox("Choose a table", ["Students", "Programming", "SoftSkills", "Placements"])
    df = db.fetch_dataframe(f"SELECT * FROM {table_name}")
    st.write("Data from table:", table_name)
    st.dataframe(df)

# -------------------- See Insights --------------------
elif option == "See Insights":
    st.subheader("Some Insights from Data")

    # Load SQL file
    try:
        with open("insights.sql", "r") as file:
            content = file.read()
            all_queries = [q.strip() for q in content.split(";") if q.strip()]
    except:
        st.error("Error loading SQL file.")
        all_queries = []

    titles = [
        "Average Problems Solved by Batch",
        "How Many Students Are Placed or Not",
        "Avg Mock Scores by Year",
        "Top 5 in Mock Interviews",
        "Soft Skills Scores by Batch",
        "Salary Stats by Batch",
        "Internships vs Placements",
        "Certifications by Placement",
        "Communication & Teamwork by Graduation",
        "Interview Rounds Cleared vs Status"
    ]

    # Display insights
    for i, query in enumerate(all_queries):
        st.markdown(f"### {titles[i] if i < len(titles) else 'Insight ' + str(i+1)}")
        try:
            df = db.fetch_dataframe(query)
            st.dataframe(df)

            if i == 0:
                st.bar_chart(df.set_index("course_batch")["avg_problems_solved"])
            elif i == 1:
                st.bar_chart(df.set_index("placement_status")["student_count"])
            elif i == 2:
                st.line_chart(df.set_index("enrollment_year")["avg_mock_score"])
            elif i == 3:
                st.bar_chart(df.set_index("name")["mock_interview_score"])
            elif i == 4:
                st.line_chart(df.set_index("course_batch")["avg_soft_skills_score"])
            elif i == 5:
                st.bar_chart(df.set_index("course_batch")["avg_package"])
            elif i == 6:
                st.bar_chart(df.set_index("internships_completed")["placed_count"])
            elif i == 7:
                st.bar_chart(df.set_index("placement_status")["avg_certifications"])
            elif i == 8:
                st.line_chart(df.set_index("graduation_year")[["avg_communication", "avg_teamwork"]])
            elif i == 9:
                st.line_chart(df.set_index("interview_rounds_cleared")["placed_count"])
        except Exception as e:
            st.error("Something went wrong: " + str(e))
