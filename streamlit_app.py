import streamlit as st
from src.db_manager import DatabaseManager  # this file helps to connect to the database and run SQL

# connect to database using the class
db = DatabaseManager()

# setup the Streamlit page
st.set_page_config(page_title="Placement App", layout="wide")
st.title("My Placement Eligibility App (Beginner Version)")

# Let user choose what they want to do
option = st.sidebar.radio("Choose one option", ["Check Eligible Students", "See Table Data", "See Insights"])


if option == "Check Eligible Students":
    st.sidebar.header("Set Your Filters")

    # take input from user using sliders
    min_problems = st.sidebar.slider("Minimum Problems Solved", 0, 150, 30)
    min_softskills = st.sidebar.slider("Minimum Soft Skills Average", 0, 100, 60)
    min_mock = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 50)

    # SQL query with 3 filters
    sql = """
    SELECT s.student_id, s.name, s.email, s.course_batch, p.problems_solved,
           ss.communication, ss.teamwork, ss.presentation,
           pl.mock_interview_score, pl.placement_status
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
    JOIN SoftSkills ss ON s.student_id = ss.student_id
    JOIN Placements pl ON s.student_id = pl.student_id
    WHERE p.problems_solved >= ?
      AND (
        (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6
      ) >= ?
      AND pl.mock_interview_score >= ?
    ORDER BY p.problems_solved DESC
    """

    # run the query with filters
    results = db.fetch_dataframe(sql, params=(min_problems, min_softskills, min_mock))

    # show the result
    st.subheader("Students who matched the filters")
    st.write("Number of students found: ", results.shape[0])
    st.dataframe(results)

    # download option
    st.download_button("Download as CSV", data=results.to_csv(index=False), file_name="eligible_students.csv", mime="text/csv")


elif option == "See Table Data":
    st.subheader("See any Table")
    table_name = st.selectbox("Choose a table", ["Students", "Programming", "SoftSkills", "Placements"])

    sql = f"SELECT * FROM {table_name}"
    df = db.fetch_dataframe(sql)

    st.write("Data from table:", table_name)
    st.dataframe(df)



elif option == "See Insights":
    st.subheader("Some Insights from Data")

    # try loading SQL file
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

    # loop through all insights and display
    for i in range(len(all_queries)):
        st.markdown(f"### {titles[i] if i < len(titles) else 'Insight ' + str(i+1)}")
        try:
            df = db.fetch_dataframe(all_queries[i])
            st.dataframe(df)

            #Visualizations 
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
