-- Database Creation
create database students_database;
use students_database;
-- Students Table
CREATE TABLE students_table(
stu_id INT AUTO_INCREMENT PRIMARY KEY,
stu_name VARCHAR(255) NOT NULL, stu_age INT,
stu_gender VARCHAR(25), stu_email_id VARCHAR(255),
stu_phone_number BIGINT, stu_enrolled_year YEAR, stu_enrolled_course_name VARCHAR(255),
stu_batch_type VARCHAR(100), stu_batch_code INT, stu_city VARCHAR(100), stu_graduation_year YEAR);
-- Programming Table
CREATE TABLE programming_table(
programming_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
programming_languages VARCHAR(50), total_attendance_percentage INT, total_codekata_problems_solved INT,
no_of_assessments_completed INT, no_of_mini_projects_completed INT,
no_of_certifications_earned INT, cumulative_test_completed VARCHAR(50), overall_cumulative_test_percentage INT, 
latest_project_score INT, FOREIGN KEY (stu_id) REFERENCES students_table(stu_id));
-- Soft Skills Table
CREATE TABLE soft_skills_table(
soft_skill_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
communication_skills_score INT, teamwork_skills_score INT,
presentation_skills_score INT, leadership_skills_score INT,
critical_thinking_skills_scores INT, interpersonal_skills_score INT,
FOREIGN KEY (stu_id) REFERENCES students_table(stu_id));
-- Placements Table
CREATE TABLE placements_table(
placement_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
mock_interview_score TINYINT, no_of_internships_completed INT,
placement_status VARCHAR(50), company_name VARCHAR(255),
placement_package DECIMAL(10, 2), interview_rounds_cleared INT,
placement_date DATE, FOREIGN KEY (stu_id) REFERENCES students_table(stu_id));
select * from students_table;
select * from programming_table;
select * from soft_skills_table;
select * from placements_table;
UPDATE placements_table
-- NULL Value Declaration for Columns
SET placement_package = NULL,
company_name = NULL,
placement_date = NULL
WHERE placement_status = 'Not Placed';