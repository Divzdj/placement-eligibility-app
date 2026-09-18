from faker import Faker
import random

if __package__:
    from .db_manager import DatabaseManager
else:
    from db_manager import DatabaseManager


def seed_demo_data(db):
    """Seed an entirely empty database once, including during concurrent startup."""
    db.conn.execute("BEGIN IMMEDIATE")
    try:
        tables = ("Students", "Programming", "SoftSkills", "Placements")
        if any(db.conn.execute(f'SELECT 1 FROM "{table}" LIMIT 1').fetchone() for table in tables):
            db.conn.rollback()
            return False
        fake = Faker()
        fake.seed_instance(42)
        rng = random.Random(42)
        # Helper lists
        batches = ["Batch A", "Batch B", "Batch C"]
        placement_statuses = ["Placed", "Not Placed"]

        # Generate 100 students
        for student_id in range(1, 101):
            # -------------------- Students --------------------
            name = fake.name()
            age = rng.randint(20, 25)
            gender = rng.choice(["Male", "Female", "Other"])
            email = fake.email()
            course_batch = rng.choice(batches)
            enrollment_year = rng.randint(2020, 2023)
            graduation_year = enrollment_year + 4

            db.cursor.execute('''
                INSERT INTO Students (student_id, name, age, gender, email, course_batch, enrollment_year, graduation_year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, name, age, gender, email, course_batch, enrollment_year, graduation_year))

            # -------------------- Programming --------------------
            problems_solved = rng.randint(10, 200)
            certifications_earned = rng.randint(0, 10)

            db.cursor.execute('''
                INSERT INTO Programming (student_id, problems_solved, certifications_earned)
                VALUES (?, ?, ?)
            ''', (student_id, problems_solved, certifications_earned))

            # -------------------- SoftSkills --------------------
            communication = rng.randint(1, 10)
            teamwork = rng.randint(1, 10)
            presentation = rng.randint(1, 10)
            leadership = rng.randint(1, 10)
            critical_thinking = rng.randint(1, 10)
            interpersonal_skills = rng.randint(1, 10)

            db.cursor.execute('''
                INSERT INTO SoftSkills (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills))

            # -------------------- Placements --------------------
            placement_status = rng.choice(placement_statuses)
            mock_interview_score = round(rng.uniform(50, 100), 2)
            placement_package = round(rng.uniform(3.0, 15.0), 2) if placement_status == "Placed" else None
            internships_completed = rng.randint(0, 5)
            interview_rounds_cleared = rng.randint(0, 5)

            db.cursor.execute('''
                INSERT INTO Placements (student_id, placement_status, mock_interview_score, placement_package, internships_completed, interview_rounds_cleared)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, placement_status, mock_interview_score, placement_package, internships_completed, interview_rounds_cleared))

        db.conn.commit()
        return True
    except Exception:
        db.conn.rollback()
        raise


if __name__ == "__main__":
    db = DatabaseManager()
    try:
        db.initialize()
        created = seed_demo_data(db)
        print("Generated 100 demo students." if created else "Existing records preserved; no demo data added.")
    finally:
        db.close()
