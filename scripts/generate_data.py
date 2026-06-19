# ============================================================
#  Data Generation Script — CSV, JSON, Excel
#  Author: Roselyn G. Polanco González (2309184)
#  Role:   Data Generation & Instrumentation
#
#  Research question:
#  Do books tagged with more than one subject receive more
#  detail page views than books tagged with a single subject?
#  → Generate books with varying tag counts + simulated view events
# ============================================================

# TODO (Rous): Generate sample data for the following entities:
#
#  1. students.csv / students.json
#     Fields: student_id, name, career, semester
#     Note: include students from all 4 career programs (for Diego's question)
#
#  2. books.csv / books.json
#     Fields: book_id, title, author, description
#     Mix: some books with 1 subject tag, others with 2-4 tags
#     → Key variable for Rous's analysis
#
#  3. book_subjects.csv
#     Fields: book_id, subject_id
#     Vary the number of subjects per book deliberately
#
#  4. book_views.csv
#     Fields: view_id, book_id, student_id, career, viewed_at
#     → Needed for Diego's career-distribution analysis
#     → Needed for Rous's single vs. multi-tag view count analysis
#
#  5. search_events.csv
#     Fields: event_id, student_id, query, filter_used (bool), clicked (bool)
#     → Needed for Arturo's conversion rate analysis
#
#  6. sessions.csv
#     Fields: session_id, student_id, start_time, end_time, books_browsed, subjects_visited
#     → Needed for Mau's duration vs. subject count analysis
#     → Needed for Rodri's browsing depth vs. save probability
#
#  7. saved_books.csv
#     Fields: save_id, student_id, book_id, browsing_depth_at_save
#     → Key variable for Rodri's analysis
#
#  8. grades_report.xlsx  (summary sheet)
#     Sheet 1: Books with tag count + view count summary
#     Sheet 2: Session stats per student

import csv
import json
import os

BASE    = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE, "../data/csv")
JSON_DIR= os.path.join(BASE, "../data/json")
XLS_DIR = os.path.join(BASE, "../data/excel")

for d in [CSV_DIR, JSON_DIR, XLS_DIR]:
    os.makedirs(d, exist_ok=True)

if __name__ == "__main__":
    print("TODO: implement data generation — Rous (2309184)")
