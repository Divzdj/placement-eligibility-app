from faker import Faker
import random
<<<<<<< HEAD
from db_manager import DatabaseManager
=======
import sqlite3
>>>>>>> 253a2f31fd5fec133a7a0fcd55b485719b315d1b

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

<<<<<<< HEAD
# Initialize DB
db = DatabaseManager()
db.create_students_table()
db.create_programming_table()
db.create_softskills_table()
db.create_placements_table()

# Helper lists
batches = ["Batch A", "Batch B", "Batch C"]
placement_statuses = ["Placed", "Not Placed"]

# Generate 100 students
for student_id in range(1, 101):
    # -------------------- Students --------------------
    name = fake.name()
    age = random.randint(20, 25)
    gender = random.choice(["Male", "Female", "Other"])
    email = fake.email()
    course_batch = random.choice(batches)
    enrollment_year = random.randint(2020, 2023)
    graduation_year = enrollment_year + 4

    db.cursor.execute('''
        INSERT INTO Students (student_id, name, age, gender, email, course_batch, enrollment_year, graduation_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, name, age, gender, email, course_batch, enrollment_year, graduation_year))

    # -------------------- Programming --------------------
    problems_solved = random.randint(10, 200)
    certifications_earned = random.randint(0, 10)

    db.cursor.execute('''
        INSERT INTO Programming (student_id, problems_solved, certifications_earned)
        VALUES (?, ?, ?)
    ''', (student_id, problems_solved, certifications_earned))

    # -------------------- SoftSkills --------------------
    communication = random.randint(1, 10)
    teamwork = random.randint(1, 10)
    presentation = random.randint(1, 10)
    leadership = random.randint(1, 10)
    critical_thinking = random.randint(1, 10)
    interpersonal_skills = random.randint(1, 10)

    db.cursor.execute('''
        INSERT INTO SoftSkills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills))

    # -------------------- Placements --------------------
    placement_status = random.choice(placement_statuses)
    mock_interview_score = round(random.uniform(50, 100), 2)
    placement_package = round(random.uniform(3.0, 15.0), 2) if placement_status == "Placed" else None
    internships_completed = random.randint(0, 5)
    interview_rounds_cleared = random.randint(0, 5)

    db.cursor.execute('''
        INSERT INTO Placements (student_id, placement_status, mock_interview_score, placement_package, internships_completed, interview_rounds_cleared)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, placement_status, mock_interview_score, placement_package, internships_completed, interview_rounds_cleared))

# Commit and close
db.conn.commit()
db.close()

print("Database generated with 100 students and related tables!")
=======
# Connect to SQLite DB
conn = sqlite3.connect("placement.db")
cursor = conn.cursor()

# Drop tables if they already exist (for repeatability during development)
cursor.executescript("""
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Programming;
DROP TABLE IF EXISTS SoftSkills;
DROP TABLE IF EXISTS Placements;
""")

# Create tables
cursor.execute("""
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT UNIQUE
);
""")

cursor.execute("""
CREATE TABLE Programming (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    language TEXT,
    proficiency_level TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
""")

cursor.execute("""
CREATE TABLE SoftSkills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    communication_score INTEGER,
    leadership_score INTEGER,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
""")

cursor.execute("""
CREATE TABLE Placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    placed BOOLEAN,
    company TEXT,
    package REAL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);
""")

# Insert students
num_students = random.randint(100, 150)
students = []

for student_id in range(1, num_students + 1):
    name = fake.name()
    age = random.randint(20, 25)
    gender = random.choice(["Male", "Female", "Other"])
    email = fake.unique.email()
    students.append((student_id, name, age, gender, email))

cursor.executemany("INSERT INTO Students VALUES (?, ?, ?, ?, ?)", students)

# Insert programming data
languages = ["Python", "Java", "C++", "JavaScript", "SQL"]
proficiency = ["Beginner", "Intermediate", "Advanced"]

for student in students:
    student_id = student[0]
    lang = random.choice(languages)
    prof = random.choice(proficiency)
    cursor.execute("INSERT INTO Programming (student_id, language, proficiency_level) VALUES (?, ?, ?)",
                   (student_id, lang, prof))

# Insert soft skills
for student in students:
    student_id = student[0]
    comm_score = random.randint(60, 100)
    leader_score = random.randint(60, 100)
    cursor.execute("INSERT INTO SoftSkills (student_id, communication_score, leadership_score) VALUES (?, ?, ?)",
                   (student_id, comm_score, leader_score))

# Insert placement data
companies = ["TCS", "Infosys", "Wipro", "Google", "Amazon", "None"]
for student in students:
    student_id = student[0]
    placed = random.choice([True, False])
    company = random.choice(companies[:-1]) if placed else "None"
    package = round(random.uniform(3, 15), 2) if placed else 0.0
    cursor.execute("INSERT INTO Placements (student_id, placed, company, package) VALUES (?, ?, ?, ?)",
                   (student_id, placed, company, package))

# Commit and close
conn.commit()
conn.close()

print("Database 'placement.db' generated with Students, Programming, SoftSkills, and Placements tables.")
>>>>>>> 253a2f31fd5fec133a7a0fcd55b485719b315d1b
