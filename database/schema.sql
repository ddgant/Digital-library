-- ============================================================
--  TeamX Academic Management Platform — Database Schema
--  Author: Mauricio Gabriel Ramírez Rubio (2309192)
--  Role:   Database Design
-- ============================================================

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;

-- ─────────────────────────────────────────
-- STUDENTS
-- ─────────────────────────────────────────
CREATE TABLE students (
    student_id   SERIAL PRIMARY KEY,
    control_num  VARCHAR(10)  UNIQUE NOT NULL,  -- e.g. 2309067
    first_name   VARCHAR(80)  NOT NULL,
    last_name    VARCHAR(80)  NOT NULL,
    email        VARCHAR(120) UNIQUE NOT NULL,
    phone        VARCHAR(20),
    birth_date   DATE,
    major        VARCHAR(100),
    semester     SMALLINT     CHECK (semester BETWEEN 1 AND 12),
    gpa          NUMERIC(4,2) DEFAULT 0.00,
    is_active    BOOLEAN      DEFAULT TRUE,
    created_at   TIMESTAMP    DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- PROFESSORS
-- ─────────────────────────────────────────
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    employee_id  VARCHAR(10)  UNIQUE NOT NULL,
    first_name   VARCHAR(80)  NOT NULL,
    last_name    VARCHAR(80)  NOT NULL,
    email        VARCHAR(120) UNIQUE NOT NULL,
    department   VARCHAR(100),
    is_active    BOOLEAN      DEFAULT TRUE,
    created_at   TIMESTAMP    DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- COURSES
-- ─────────────────────────────────────────
CREATE TABLE courses (
    course_id    SERIAL PRIMARY KEY,
    course_code  VARCHAR(20)  UNIQUE NOT NULL,  -- e.g. CS301
    title        VARCHAR(150) NOT NULL,
    description  TEXT,
    credits      SMALLINT     NOT NULL CHECK (credits BETWEEN 1 AND 10),
    semester     VARCHAR(20)  NOT NULL,          -- e.g. 2025-A
    schedule     VARCHAR(100),                   -- e.g. Mon/Wed 10:00-11:30
    classroom    VARCHAR(30),
    max_capacity SMALLINT     DEFAULT 30,
    professor_id INT          REFERENCES professors(professor_id) ON DELETE SET NULL,
    is_active    BOOLEAN      DEFAULT TRUE,
    created_at   TIMESTAMP    DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- ENROLLMENTS
-- ─────────────────────────────────────────
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id    INT  NOT NULL REFERENCES students(student_id)  ON DELETE CASCADE,
    course_id     INT  NOT NULL REFERENCES courses(course_id)    ON DELETE CASCADE,
    enrolled_at   TIMESTAMP DEFAULT NOW(),
    status        VARCHAR(20) DEFAULT 'active'
                  CHECK (status IN ('active', 'dropped', 'completed')),
    UNIQUE (student_id, course_id)
);

-- ─────────────────────────────────────────
-- GRADES
-- ─────────────────────────────────────────
CREATE TABLE grades (
    grade_id      SERIAL PRIMARY KEY,
    enrollment_id INT          NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE CASCADE,
    partial       SMALLINT     NOT NULL CHECK (partial BETWEEN 1 AND 3),
    score         NUMERIC(5,2) CHECK (score BETWEEN 0 AND 100),
    letter_grade  CHAR(2),
    submitted_at  TIMESTAMP    DEFAULT NOW(),
    UNIQUE (enrollment_id, partial)
);

-- ─────────────────────────────────────────
-- ATTENDANCE
-- ─────────────────────────────────────────
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    enrollment_id INT      NOT NULL REFERENCES enrollments(enrollment_id) ON DELETE CASCADE,
    session_date  DATE     NOT NULL,
    status        VARCHAR(10) DEFAULT 'present'
                  CHECK (status IN ('present', 'absent', 'late', 'excused')),
    notes         TEXT,
    UNIQUE (enrollment_id, session_date)
);

-- ─────────────────────────────────────────
-- INDEXES for performance
-- ─────────────────────────────────────────
CREATE INDEX idx_students_control    ON students(control_num);
CREATE INDEX idx_courses_code        ON courses(course_code);
CREATE INDEX idx_enrollments_student ON enrollments(student_id);
CREATE INDEX idx_enrollments_course  ON enrollments(course_id);
CREATE INDEX idx_grades_enrollment   ON grades(enrollment_id);
CREATE INDEX idx_attendance_date     ON attendance(session_date);
