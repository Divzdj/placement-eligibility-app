-- insights.sql

-- 1. Average problems solved by course batch
SELECT s.course_batch, 
       ROUND(AVG(p.problems_solved), 2) AS avg_problems_solved
FROM Students s
JOIN Programming p ON s.student_id = p.student_id
GROUP BY s.course_batch
ORDER BY avg_problems_solved DESC;

-- 2. Count of students by placement status
SELECT placement_status, COUNT(*) AS student_count
FROM Placements
GROUP BY placement_status
ORDER BY student_count DESC;

-- 3. Average mock interview score by enrollment year
SELECT s.enrollment_year, 
       ROUND(AVG(pl.mock_interview_score), 2) AS avg_mock_score
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
GROUP BY s.enrollment_year
ORDER BY s.enrollment_year;

-- 4. Top 5 students by mock interview score (including name and email)
SELECT s.student_id, s.name, s.email, pl.mock_interview_score
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
ORDER BY pl.mock_interview_score DESC
LIMIT 5;

-- 5. Distribution of Average Soft Skills Score by Batch
SELECT 
    s.course_batch,
    AVG(
        (ss.communication + ss.teamwork + ss.presentation + ss.leadership +
         ss.critical_thinking + ss.interpersonal_skills) / 6.0
    ) AS avg_soft_skills_score
FROM Students s
JOIN SoftSkills ss ON s.student_id = ss.student_id
GROUP BY s.course_batch
ORDER BY avg_soft_skills_score DESC;

-- 6. Placement package statistics by course batch
SELECT s.course_batch,
       COUNT(pl.placement_package) AS placed_students,
       ROUND(AVG(pl.placement_package), 2) AS avg_package,
       MIN(pl.placement_package) AS min_package,
       MAX(pl.placement_package) AS max_package
FROM Students s
JOIN Placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Placed'
GROUP BY s.course_batch
ORDER BY avg_package DESC;

-- 7. Number of internships completed vs placement readiness
SELECT pl.internships_completed,
       COUNT(*) AS student_count,
       SUM(CASE WHEN pl.placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_count
FROM Placements pl
GROUP BY pl.internships_completed
ORDER BY pl.internships_completed;

-- 8. Average programming certifications earned by placement status
SELECT pl.placement_status,
       ROUND(AVG(p.certifications_earned), 2) AS avg_certifications
FROM Placements pl
JOIN Programming p ON pl.student_id = p.student_id
GROUP BY pl.placement_status
ORDER BY avg_certifications DESC;

-- 9. Average scores for communication and teamwork by graduation year
SELECT s.graduation_year,
       ROUND(AVG(ss.communication), 2) AS avg_communication,
       ROUND(AVG(ss.teamwork), 2) AS avg_teamwork
FROM Students s
JOIN SoftSkills ss ON s.student_id = ss.student_id
GROUP BY s.graduation_year
ORDER BY s.graduation_year;

-- 10. Number of interview rounds cleared vs placement status
SELECT pl.interview_rounds_cleared,
       COUNT(*) AS student_count,
       SUM(CASE WHEN pl.placement_status = 'Placed' THEN 1 ELSE 0 END) AS placed_count
FROM Placements pl
GROUP BY pl.interview_rounds_cleared
ORDER BY pl.interview_rounds_cleared DESC;
