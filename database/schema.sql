-- ============================================================
--  TeamX Digital Library Platform — Database Schema
--  Author: Mauricio Gabriel Ramírez Rubio (2309192)
--  Role:   Database Design
--
--  This schema supports all five research questions:
--  [Arturo] filter usage vs. search-to-click conversion
--  [Diego]  subject traffic across the four career programs
--  [Rous]   single-tag vs. multi-tag book view counts
--  [Rodri]  browsing depth vs. save probability
--  [Mau]    session duration vs. distinct subjects visited
-- ============================================================

DROP TABLE IF EXISTS saved_books      CASCADE;
DROP TABLE IF EXISTS session_subjects CASCADE;
DROP TABLE IF EXISTS sessions         CASCADE;
DROP TABLE IF EXISTS search_events    CASCADE;
DROP TABLE IF EXISTS book_views       CASCADE;
DROP TABLE IF EXISTS book_subjects    CASCADE;
DROP TABLE IF EXISTS subjects         CASCADE;
DROP TABLE IF EXISTS books            CASCADE;
DROP TABLE IF EXISTS students         CASCADE;

-- ─────────────────────────────────────────
-- STUDENTS  (career affiliation → Diego's question)
-- ─────────────────────────────────────────
CREATE TABLE students (
    student_id  SERIAL PRIMARY KEY,
    control_num VARCHAR(10) UNIQUE NOT NULL,
    full_name   VARCHAR(120) NOT NULL,
    email       VARCHAR(120) UNIQUE NOT NULL,
    career      VARCHAR(60)  NOT NULL,   -- one of the four career programs
    semester    SMALLINT     CHECK (semester BETWEEN 1 AND 12),
    created_at  TIMESTAMP    DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- SUBJECTS  (subject areas / tags)
-- ─────────────────────────────────────────
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    name       VARCHAR(80) UNIQUE NOT NULL
);

-- ─────────────────────────────────────────
-- BOOKS
-- ─────────────────────────────────────────
CREATE TABLE books (
    book_id     SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    author      VARCHAR(120),
    year        SMALLINT,
    description TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- ─────────────────────────────────────────
-- BOOK ↔ SUBJECT (many-to-many → Rous's question)
-- ─────────────────────────────────────────
CREATE TABLE book_subjects (
    book_id    INT NOT NULL REFERENCES books(book_id)       ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    PRIMARY KEY (book_id, subject_id)
);

-- ─────────────────────────────────────────
-- BOOK VIEWS  (detail-page views → Diego & Rous)
-- ─────────────────────────────────────────
CREATE TABLE book_views (
    view_id    SERIAL PRIMARY KEY,
    book_id    INT NOT NULL REFERENCES books(book_id)       ON DELETE CASCADE,
    student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    career     VARCHAR(60) NOT NULL,    -- denormalized for fast career analysis
    viewed_at  TIMESTAMP   NOT NULL
);

-- ─────────────────────────────────────────
-- SEARCH EVENTS  (filter usage + click → Arturo)
-- ─────────────────────────────────────────
CREATE TABLE search_events (
    event_id    SERIAL PRIMARY KEY,
    student_id  INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    query       VARCHAR(200),
    filter_used BOOLEAN NOT NULL DEFAULT FALSE,
    clicked     BOOLEAN NOT NULL DEFAULT FALSE,
    searched_at TIMESTAMP NOT NULL
);

-- ─────────────────────────────────────────
-- SESSIONS  (duration + browsing depth → Mau & Rodri)
-- ─────────────────────────────────────────
CREATE TABLE sessions (
    session_id       SERIAL PRIMARY KEY,
    student_id       INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    started_at       TIMESTAMP NOT NULL,
    ended_at         TIMESTAMP NOT NULL,
    duration_minutes NUMERIC(6,2) NOT NULL,
    books_browsed    SMALLINT NOT NULL DEFAULT 0,   -- browsing depth → Rodri
    saved_final      BOOLEAN  NOT NULL DEFAULT FALSE -- did they save at the end? → Rodri
);

-- ─────────────────────────────────────────
-- SESSION ↔ SUBJECT  (distinct subjects per session → Mau)
-- ─────────────────────────────────────────
CREATE TABLE session_subjects (
    session_id INT NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
    subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    PRIMARY KEY (session_id, subject_id)
);

-- ─────────────────────────────────────────
-- SAVED BOOKS  (→ Rodri)
-- ─────────────────────────────────────────
CREATE TABLE saved_books (
    save_id                SERIAL PRIMARY KEY,
    student_id             INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    book_id                INT NOT NULL REFERENCES books(book_id)       ON DELETE CASCADE,
    browsing_depth_at_save SMALLINT NOT NULL,
    saved_at               TIMESTAMP NOT NULL,
    UNIQUE (student_id, book_id)
);

-- ─────────────────────────────────────────
-- INDEXES
-- ─────────────────────────────────────────
CREATE INDEX idx_views_book      ON book_views(book_id);
CREATE INDEX idx_views_career    ON book_views(career);
CREATE INDEX idx_booksub_book    ON book_subjects(book_id);
CREATE INDEX idx_booksub_subject ON book_subjects(subject_id);
CREATE INDEX idx_search_filter   ON search_events(filter_used);
CREATE INDEX idx_sessions_student ON sessions(student_id);
CREATE INDEX idx_saved_student   ON saved_books(student_id);
