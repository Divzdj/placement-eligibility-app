import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="placement.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    # -------------------- Table creation --------------------
    def create_students_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                email TEXT,
                course_batch TEXT,
                enrollment_year INTEGER,
                graduation_year INTEGER
            )
        ''')
        self.conn.commit()

    def create_programming_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Programming (
                student_id INTEGER,
                problems_solved INTEGER,
                certifications_earned INTEGER,
                FOREIGN KEY(student_id) REFERENCES Students(student_id)
            )
        ''')
        self.conn.commit()

    def create_softskills_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS SoftSkills (
                student_id INTEGER,
                communication INTEGER,
                teamwork INTEGER,
                presentation INTEGER,
                leadership INTEGER,
                critical_thinking INTEGER,
                interpersonal_skills INTEGER,
                FOREIGN KEY(student_id) REFERENCES Students(student_id)
            )
        ''')
        self.conn.commit()

    def create_placements_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Placements (
                student_id INTEGER,
                placement_status TEXT,
                mock_interview_score REAL,
                placement_package REAL,
                internships_completed INTEGER,
                interview_rounds_cleared INTEGER,
                FOREIGN KEY(student_id) REFERENCES Students(student_id)
            )
        ''')
        self.conn.commit()

    # -------------------- Query helper --------------------
    def fetch_dataframe(self, query, params=None):
        """
        Run a SELECT query and return a pandas DataFrame.
        params: optional tuple of parameters for parameterized queries.
        """
        if params:
            df = pd.read_sql_query(query, self.conn, params=params)
        else:
            df = pd.read_sql_query(query, self.conn)
        return df

    # -------------------- Close connection --------------------
    def close(self):
        self.conn.close()
