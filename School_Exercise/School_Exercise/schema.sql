-- Create the students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_name TEXT
);

-- Create the courses table
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name TEXT
);

-- Create the enrollments table
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);