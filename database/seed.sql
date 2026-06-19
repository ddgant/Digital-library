-- ============================================================
--  TeamX Academic Management Platform — Seed Data
--  Author: Mauricio Gabriel Ramírez Rubio (2309192)
-- ============================================================

-- Professors
INSERT INTO professors (employee_id, first_name, last_name, email, department) VALUES
('P001', 'Ana',    'Torres',   'a.torres@universidad.mx',  'Computer Science'),
('P002', 'Luis',   'Herrera',  'l.herrera@universidad.mx', 'Data Engineering'),
('P003', 'María',  'Fuentes',  'm.fuentes@universidad.mx', 'Software Design');

-- Students
INSERT INTO students (control_num, first_name, last_name, email, major, semester) VALUES
('2309017', 'Cesar Arturo', 'Balam Euan',       'arturo@uni.mx',   'Computer Science', 4),
('2309067', 'Diego',        'De Gante Pérez',   'diego@uni.mx',    'Computer Science', 4),
('2309184', 'Roselyn G.',   'Polanco González', 'rous@uni.mx',     'Data Engineering', 4),
('2309192', 'Mauricio',     'Ramírez Rubio',    'mauricio@uni.mx', 'Computer Science', 4),
('2309091', 'Rodrigo',      'Garcia Martinez',  'rodrigo@uni.mx',  'Software Design',  4),
('2300001', 'Laura',        'Méndez Ruiz',      'laura@uni.mx',    'Computer Science', 3),
('2300002', 'Andrés',       'Villarreal López', 'andres@uni.mx',   'Data Engineering', 5);

-- Courses
INSERT INTO courses (course_code, title, credits, semester, schedule, classroom, max_capacity, professor_id) VALUES
('CS301', 'Database Systems',        4, '2025-A', 'Mon/Wed 08:00-09:30', 'F-201', 35, 1),
('CS302', 'Web Development',         4, '2025-A', 'Tue/Thu 10:00-11:30', 'F-105', 30, 3),
('DE201', 'Data Engineering Basics', 3, '2025-A', 'Mon/Fri 12:00-13:00', 'B-302', 25, 2),
('CS401', 'API Design & REST',       3, '2025-A', 'Wed/Fri 14:00-15:30', 'F-203', 28, 1);

-- Enrollments
INSERT INTO enrollments (student_id, course_id, status) VALUES
(1, 1, 'active'), (1, 2, 'active'),
(2, 1, 'active'), (2, 4, 'active'),
(3, 3, 'active'), (3, 1, 'active'),
(4, 1, 'active'), (4, 4, 'active'),
(5, 4, 'active'), (5, 2, 'active'),
(6, 2, 'active'),
(7, 3, 'active');

-- Grades (partial 1)
INSERT INTO grades (enrollment_id, partial, score, letter_grade) VALUES
(1, 1, 88.0, 'B+'),
(2, 1, 91.5, 'A' ),
(3, 1, 76.0, 'C+'),
(4, 1, 95.0, 'A' ),
(5, 1, 83.0, 'B' ),
(6, 1, 70.0, 'C' ),
(7, 1, 89.0, 'B+'),
(8, 1, 92.0, 'A' ),
(9, 1, 85.0, 'B+'),
(10,1, 78.0, 'C+');

-- Attendance samples
INSERT INTO attendance (enrollment_id, session_date, status) VALUES
(1, '2025-02-03', 'present'),
(1, '2025-02-05', 'present'),
(1, '2025-02-10', 'absent'),
(2, '2025-02-03', 'present'),
(2, '2025-02-05', 'late'),
(3, '2025-02-03', 'present'),
(3, '2025-02-05', 'present');
