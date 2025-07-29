import os
import random
import sqlite3
import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)

# ------------------- STUDENTS TABLE -------------------
def generate_students(num_students=120):
    students = []
    for student_id in range(1, num_students + 1):
        name = fake.name()
        age = random.randint(20, 25)
        gender = random.choice(["Male", "Female", "Other"])
        email = fake.email()
        phone = fake.phone_number()
        enrollment_year = random.choice([2019, 2020, 2021, 2022])
        course_batch = random.choice(["Batch A", "Batch B", "Batch C"])
        city = fake.city()
        graduation_year = enrollment_year + 4

        students.append({
            "student_id": student_id,
            "name": name,
            "age": age,
            "gender": gender,
            "email": email,
            "phone": phone,
            "enrollment_year": enrollment_year,
            "course_batch": course_batch,
            "city": city,
            "graduation_year": graduation_year
        })
    return students

# ------------------- PROGRAMMING TABLE -------------------
def generate_programming(student_ids):
    programming_data = []
    programming_id = 1
    languages = ["Python", "SQL", "Java", "C++"]

    for student_id in student_ids:
        for _ in range(random.randint(1, 2)):  # 1–2 records per student
            language = random.choice(languages)
            programming_data.append({
                "programming_id": programming_id,
                "student_id": student_id,
                "language": language,
                "problems_solved": random.randint(10, 150),
                "assessments_completed": random.randint(1, 5),
                "mini_projects": random.randint(0, 3),
                "certifications_earned": random.randint(0, 2),
                "latest_project_score": random.randint(50, 100)
            })
            programming_id += 1

    return programming_data

# ------------------- SOFT SKILLS TABLE -------------------
def generate_soft_skills(student_ids):
    soft_skills_data = []
    for soft_skill_id, student_id in enumerate(student_ids, start=1):
        soft_skills_data.append({
            "soft_skill_id": soft_skill_id,
            "student_id": student_id,
            "communication": random.randint(40, 100),
            "teamwork": random.randint(40, 100),
            "presentation": random.randint(40, 100),
            "leadership": random.randint(40, 100),
            "critical_thinking": random.randint(40, 100),
            "interpersonal_skills": random.randint(40, 100)
        })
    return soft_skills_data

# ------------------- PLACEMENTS TABLE -------------------
def generate_placements(student_ids):
    placements_data = []
    for placement_id, student_id in enumerate(student_ids, start=1):
        status = random.choice(["Ready", "Not Ready", "Placed"])
        company = fake.company() if status == "Placed" else None
        package = round(random.uniform(3.0, 15.0), 2) if status == "Placed" else None
        placement_date = fake.date_between(start_date='-2y', end_date='today') if status == "Placed" else None

        placements_data.append({
            "placement_id": placement_id,
            "student_id": student_id,
            "mock_interview_score": random.randint(40, 100),
            "internships_completed": random.randint(0, 3),
            "placement_status": status,
            "company_name": company,
            "placement_package": package,
            "interview_rounds_cleared": random.randint(0, 5),
            "placement_date": placement_date
        })
    return placements_data

# ------------------- MAIN EXECUTION -------------------
if __name__ == "__main__":
    # Create data folder
    os.makedirs("data", exist_ok=True)

    # ---- STUDENTS ----
    students = generate_students()
    df_students = pd.DataFrame(students)
    df_students.to_csv("data/students.csv", index=False)

    # ---- PROGRAMMING ----
    programming = generate_programming(df_students["student_id"].tolist())
    df_programming = pd.DataFrame(programming)
    df_programming.to_csv("data/programming.csv", index=False)

    # ---- SOFT SKILLS ----
    soft_skills = generate_soft_skills(df_students["student_id"].tolist())
    df_soft_skills = pd.DataFrame(soft_skills)
    df_soft_skills.to_csv("data/soft_skills.csv", index=False)

    # ---- PLACEMENTS ----
    placements = generate_placements(df_students["student_id"].tolist())
    df_placements = pd.DataFrame(placements)
    df_placements.to_csv("data/placements.csv", index=False)

    # ---- SAVE TO DATABASE ----
    conn = sqlite3.connect("data/placement.db")

    conn.execute("DROP TABLE IF EXISTS Students;")
    df_students.to_sql("Students", conn, if_exists="replace", index=False)

    conn.execute("DROP TABLE IF EXISTS Programming;")
    df_programming.to_sql("Programming", conn, if_exists="replace", index=False)

    conn.execute("DROP TABLE IF EXISTS SoftSkills;")
    df_soft_skills.to_sql("SoftSkills", conn, if_exists="replace", index=False)

    conn.execute("DROP TABLE IF EXISTS Placements;")
    df_placements.to_sql("Placements", conn, if_exists="replace", index=False)

    conn.close()

    print("All 4 tables created and saved to data/placement.db")
