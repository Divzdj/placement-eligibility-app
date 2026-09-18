import sqlite3
from pathlib import Path
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            project_dir = Path(__file__).resolve().parents[1]
            packaged_db = project_dir / "data" / "placement.db"
            legacy_db = project_dir / "placement.db"
            db_path = packaged_db if packaged_db.exists() else legacy_db
        db_path = Path(db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path, timeout=30)
        self.cursor = self.conn.cursor()

    def initialize(self):
        """Create missing tables without replacing existing student records."""
        self.create_students_table()
        self.create_programming_table()
        self.create_softskills_table()
        self.create_placements_table()
        required = {
            "Students": "student_id name email course_batch enrollment_year graduation_year",
            "Programming": "student_id problems_solved certifications_earned",
            "SoftSkills": "student_id communication teamwork presentation leadership critical_thinking interpersonal_skills",
            "Placements": "student_id placement_status mock_interview_score placement_package internships_completed interview_rounds_cleared",
        }
        for table, names in required.items():
            actual = {row[1] for row in self.conn.execute(f'PRAGMA table_info("{table}")')}
            missing = set(names.split()) - actual
            if missing:
                raise ValueError(
                    f"Database table {table} is missing required columns: {', '.join(sorted(missing))}. "
                    "Use the project's matching database schema; existing records have not been deleted."
                )

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
