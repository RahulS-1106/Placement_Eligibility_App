from faker import Faker
import random
import pymysql

# Database class to manage MySQL connection and operations
class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self, with_db=False):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database if with_db else None,
                charset='utf8mb4',
                autocommit=True
            )
            self.cursor = self.connection.cursor()
            print("Connection successful.")
        except Exception as e:
            print("Connection failed:", e)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, values=None):
        if not self.cursor:
            raise ConnectionError("Cursor is not initialized. Call connect() first.")
        self.cursor.execute(query) if values is None else self.cursor.execute(query, values)

    def fetch_all(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_placement_package_for_unplaced(self):
        query = """
            UPDATE placements_table
            SET placement_package = NULL,
                company_name = NULL,
                placement_date = NULL
            WHERE placement_status = 'Not Placed';
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Updated NULL fields for unplaced students.")
        except Exception as e:
            print("Error while updating:", e)

# DataGenerator class to handle random data generation
class DataGenerator:
    def __init__(self, num_students):
        self.num_students = num_students
        self.fake = Faker()

    def generate_student_data(self):
        students = []
        for _ in range(self.num_students):
            students.append({
                'stu_name': self.fake.name(),
                'stu_age': random.randint(18, 40),
                'stu_gender': random.choice(['Male', 'Female']),
                'stu_email_id': self.fake.email(),
                'stu_phone_number': self.fake.random_number(digits=10),
                'stu_enrolled_year': random.randint(2018, 2025),
                'stu_enrolled_course_name': random.choice(['Data Science', 'Machine Learning', 'Artificial Intelligence', 'Data Engineering', 'Digital Marketing']),
                'stu_batch_type': random.choice(['Weekend', 'Weekday']),
                'stu_batch_code': random.randint(1, 10),
                'stu_city': self.fake.city(),
                'stu_graduation_year': random.randint(2001, 2025)
            })
        return students

    def generate_programming_data(self, stu_id):
        return {
            'stu_id': stu_id,
            'programming_languages': random.choice(['Python', 'Java', 'SQL', 'C++','Javascript', 'Ruby', 'PHP']),
            'total_attendance_percentage': random.randint(1,100),
            'total_codekata_problems_solved': random.randint(1,1000),
            'no_of_assessments_completed': random.randint(1, 50),
            'no_of_mini_projects_completed': random.randint(1, 15),
            'no_of_certifications_earned': random.randint(1, 5),
            'cumulative_test_completed': random.choice(['Yes', 'No']),
            'overall_cumulative_test_percentage': random.randint(1,100),
            'latest_project_score': random.randint(1, 10)
        }

    def generate_soft_skills_data(self, stu_id):
        return {
            'stu_id': stu_id,
            'communication_skills_score': random.randint(1, 100),
            'teamwork_skills_score': random.randint(1, 100),
            'presentation_skills_score': random.randint(1, 100),
            'leadership_skills_score': random.randint(1, 100),
            'critical_thinking_skills_scores': random.randint(1, 100),
            'interpersonal_skills_score': random.randint(1, 100)
        }

    def generate_placement_data(self, stu_id):
        placement_status = random.choice(['Placed', 'Not Placed'])

        if placement_status == 'Not Placed':
            return {
                'stu_id': stu_id,
                'mock_interview_score': random.randint(1, 100),
                'no_of_internships_completed': random.randint(1, 10),
                'placement_status': placement_status,
                'company_name': None,
                'placement_package': None,
                'interview_rounds_cleared': random.randint(1, 5),
                'placement_date': None
            }
        else:
            return {
                'stu_id': stu_id,
                'mock_interview_score': random.randint(1, 100),
                'no_of_internships_completed': random.randint(1, 10),
                'placement_status': placement_status,
                'company_name': self.fake.company(),
                'placement_package': round(random.uniform(300000, 2500000), 2),
                'interview_rounds_cleared': random.randint(1, 5),
                'placement_date': self.fake.date_this_decade()
            }

# Main app class
class PlacementApp:
    def __init__(self, db_config, num_students):
        self.db = Database(**db_config)
        self.data_gen = DataGenerator(num_students)

    def setup_database(self):
        self.db.connect()
        self.db.execute_query("CREATE DATABASE IF NOT EXISTS students_database")
        self.db.close()

        self.db.connect(with_db=True)
        self.db.execute_query('''CREATE TABLE IF NOT EXISTS students_table(
            stu_id INT AUTO_INCREMENT PRIMARY KEY,
            stu_name VARCHAR(255) NOT NULL, stu_age INT,
            stu_gender VARCHAR(25), stu_email_id VARCHAR(255),
            stu_phone_number BIGINT, stu_enrolled_year YEAR, stu_enrolled_course_name VARCHAR(255),
            stu_batch_type VARCHAR(100), stu_batch_code INT, stu_city VARCHAR(100), stu_graduation_year YEAR
        )''')

        self.db.execute_query('''CREATE TABLE IF NOT EXISTS programming_table(
            programming_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
            programming_languages VARCHAR(50), total_attendance_percentage INT, total_codekata_problems_solved INT,
            no_of_assessments_completed INT, no_of_mini_projects_completed INT,
            no_of_certifications_earned INT, cumulative_test_completed VARCHAR(50), overall_cumulative_test_percentage INT, 
            latest_project_score INT, FOREIGN KEY (stu_id) REFERENCES students_table(stu_id)
        )''')

        self.db.execute_query('''CREATE TABLE IF NOT EXISTS soft_skills_table(
            soft_skill_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
            communication_skills_score INT, teamwork_skills_score INT,
            presentation_skills_score INT, leadership_skills_score INT,
            critical_thinking_skills_scores INT, interpersonal_skills_score INT,
            FOREIGN KEY (stu_id) REFERENCES students_table(stu_id)
        )''')

        self.db.execute_query('''CREATE TABLE IF NOT EXISTS placements_table(
            placement_id INT AUTO_INCREMENT PRIMARY KEY, stu_id INT,
            mock_interview_score TINYINT, no_of_internships_completed INT,
            placement_status VARCHAR(50), company_name VARCHAR(255),
            placement_package DECIMAL(10, 2), interview_rounds_cleared INT,
            placement_date DATE, FOREIGN KEY (stu_id) REFERENCES students_table(stu_id)
        )''')

    def generate_and_insert_data(self):
        students = self.data_gen.generate_student_data()
        for student in students:
            self.db.execute_query('''INSERT INTO students_table (
                stu_name, stu_age, stu_gender, stu_email_id, stu_phone_number,
                stu_enrolled_year, stu_enrolled_course_name, stu_batch_type,
                stu_batch_code, stu_city, stu_graduation_year
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', tuple(student.values()))
            stu_id = self.db.fetch_all("SELECT LAST_INSERT_ID()")[0][0]

            prog = self.data_gen.generate_programming_data(stu_id)
            self.db.execute_query('''INSERT INTO programming_table (
                stu_id, programming_languages, total_attendance_percentage, total_codekata_problems_solved,
                no_of_assessments_completed, no_of_mini_projects_completed,
                no_of_certifications_earned, cumulative_test_completed, overall_cumulative_test_percentage, latest_project_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', tuple(prog.values()))

            soft = self.data_gen.generate_soft_skills_data(stu_id)
            self.db.execute_query('''INSERT INTO soft_skills_table (
                stu_id, communication_skills_score, teamwork_skills_score,
                presentation_skills_score, leadership_skills_score,
                critical_thinking_skills_scores, interpersonal_skills_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)''', tuple(soft.values()))

            place = self.data_gen.generate_placement_data(stu_id)
            self.db.execute_query('''INSERT INTO placements_table (
                stu_id, mock_interview_score, no_of_internships_completed,
                placement_status, company_name, placement_package,
                interview_rounds_cleared, placement_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', tuple(place.values()))

        # Nullify fields for unplaced students
        self.db.update_placement_package_for_unplaced()

        print("\u2705 Data inserted for 500 students.")

# Run the application
if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'students_database'
    }

    app = PlacementApp(db_config, num_students=500)
    app.setup_database()
    app.generate_and_insert_data()
    app.db.close()