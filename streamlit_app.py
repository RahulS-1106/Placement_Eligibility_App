import streamlit as st
import pymysql
import pandas as pd

# Database class
class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            database='students_database',
            charset='utf8mb4'
        )

    def fetch_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, self.connection)

    def fetch_eligible_students(self, min_problems, min_soft_avg, min_attendance, min_cumulative_score,
                                cumulative_test_status, placement_status):
        base_query = """
            SELECT s.stu_name, s.stu_enrolled_course_name, s.stu_batch_code, p.total_codekata_problems_solved,
                   p.programming_languages, p.total_attendance_percentage, p. no_of_mini_projects_completed, p.cumulative_test_completed, 
                   p.overall_cumulative_test_percentage, 
                   (ss.communication_skills_score + ss.teamwork_skills_score + 
                    ss.presentation_skills_score + ss.leadership_skills_score + 
                    ss.critical_thinking_skills_scores + ss.interpersonal_skills_score)/6 AS soft_skill_avg,
                   pl.placement_status, pl.company_name, pl.interview_rounds_cleared, pl.placement_package, pl.placement_date
            FROM students_table s
            JOIN programming_table p ON s.stu_id = p.stu_id
            JOIN soft_skills_table ss ON s.stu_id = ss.stu_id
            LEFT JOIN placements_table pl ON s.stu_id = pl.stu_id
            WHERE p.total_codekata_problems_solved >= %s
            AND p.total_attendance_percentage >= %s
            AND p.overall_cumulative_test_percentage >= %s
            AND (
                ss.communication_skills_score + ss.teamwork_skills_score +
                ss.presentation_skills_score + ss.leadership_skills_score +
                ss.critical_thinking_skills_scores + ss.interpersonal_skills_score
            ) / 6 >= %s
        """
        values = [min_problems, min_attendance, min_cumulative_score, min_soft_avg]

        if cumulative_test_status != "All":
            base_query += " AND p.cumulative_test_completed = %s"
            values.append(cumulative_test_status)

        if placement_status != "All":
            base_query += " AND pl.placement_status = %s"
            values.append(placement_status)

        df = pd.read_sql(base_query, self.connection, params=values)
        return df

    def close(self):
        self.connection.close()

# Streamlit UI setup
st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("🎓:blue[Placement Eligibility Filter]")

# Sliders for numeric filters
min_problems = st.slider("Minimum CodeKata Problems Solved", 0, 1000, 250)
min_attendance = st.slider("Minimum Attendance Percentage", 0, 100, 70)
min_mini_projects_completed = st.slider("Minimum No of Mini Projects Completed", 0, 15, 5)
min_cumulative_score = st.slider("Minimum Cumulative Test Percentage", 0, 100, 70)

# Dropdowns
cumulative_test_status = st.selectbox("Cumulative Test Completed", ["Yes", "No"])
placement_status = st.selectbox("Placement Status", ["Placed", "Not Placed"])

# Action button
if st.button("Get Eligible Students"):
    with st.spinner("Fetching eligible students..."):
        db = Database()
        try:
            df = db.fetch_eligible_students(
                min_problems,
                min_attendance,
                min_mini_projects_completed,
                min_cumulative_score,
                cumulative_test_status,
                placement_status
            )
            if not df.empty:
                st.success(f"✅ Found {len(df)} eligible students.")
                st.dataframe(df)
            else:
                st.warning("❌ No students match the selected criteria.")
        finally:
            db.close()