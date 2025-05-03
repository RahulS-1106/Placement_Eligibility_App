# **Placement Eligibility Data Generation and Management System**

**Overview**

This project is designed to simulate a comprehensive student placement tracking system. It uses Python to generate realistic, synthetic data for students and stores it in a MySQL database. The goal is to create a backend-ready dataset that can be used for building data analytics dashboards or placement tracking tools.

**Purpose**

The system automates the creation of a student database that includes details about students' academic profiles, programming skills, soft skills, and placement information. It ensures logical consistency in the data, such as setting placement-related fields to NULL for students who are not placed.

**Key Features**

Automated Database Setup: The system creates a database and all required tables automatically.

Synthetic Data Generation: Generates data for a large number of students using the Faker library, ensuring each entry is unique and realistic.

Modular Design: Separate classes for database management and data generation allow for easy maintenance and scaling.

Placement Logic: Automatically sets company name, package, and placement date to NULL for students who are not placed.

Clean Closure: All database connections and cursors are properly closed after operations.

**Technologies Used**

Python: For scripting and data generation logic.

Faker Library: To generate realistic names, cities, emails, dates, and company names.

PyMySQL: For MySQL database connection and query execution.

MySQL: As the backend database to store student data.

**Project Structure**

Database Initialization: Creates the students_database and all related tables if they don't exist.

Data Generation: For each student, the script generates:

Basic student details

Programming metrics (like problems solved, attendance, test scores)

Soft skills assessment

**Placement status and related details**

Data Insertion: Each set of generated data is inserted into the respective tables using parameterized queries.

Placement Handling: If a student is not placed, the related fields (company name, package, date) are explicitly set to NULL.

**Usage**

This project is useful for:

Developers building dashboards or analytics platforms for education or training institutions.

Machine learning practitioners looking for structured, realistic datasets to train classification models (e.g., predicting placement chances).

Educational institutes wanting to simulate placement pipelines for demo or testing purposes.

**Future Enhancements**

Adding a user interface using Streamlit or Flask to visualize and filter data.

Exporting the generated data to CSV or Excel for external analysis.

Including more detailed academic performance metrics and mock test scores.****
