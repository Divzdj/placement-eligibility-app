from faker import Faker
import random
from db_manager import DatabaseManager

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

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
