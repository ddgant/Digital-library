# ============================================================
#  TeamX Digital Library — Data Loader
#  Author: Roselyn G. Polanco González (2309184)
#
#  Loads the generated CSV files into PostgreSQL in FK-safe order.
# ============================================================

import csv
import os
import sys

try:
    import psycopg2
except ImportError:
    print("[ERROR] pip install psycopg2-binary")
    sys.exit(1)

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/csv"))


def conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "teamx_library"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def load_table(cx, filename, table, columns):
    path = os.path.join(CSV_DIR, filename)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        cur = cx.cursor()
        n = 0
        skipped = 0
        placeholders = ", ".join(["%s"] * len(columns))
        collist = ", ".join(columns)
        for row in reader:
            values = [row[c] if row[c] != "" else None for c in columns]
            try:
                cur.execute(
                    f"INSERT INTO {table} ({collist}) VALUES ({placeholders}) "
                    f"ON CONFLICT DO NOTHING;", values
                )
                n += 1
            except Exception:
                cx.rollback()
                skipped += 1
                cur = cx.cursor()
        cx.commit(); cur.close()
        msg = f"[LOAD] {table:<18} {n:>5} rows"
        if skipped:
            msg += f"  (skipped {skipped})"
        print(msg)


if __name__ == "__main__":
    print("=== TeamX Library Data Loader (Rous — 2309184) ===\n")
    try:
        cx = conn()
        # FK-safe order
        load_table(cx, "students.csv", "students",
                   ["student_id", "control_num", "full_name", "email", "career", "semester"])
        load_table(cx, "subjects.csv", "subjects", ["subject_id", "name"])
        load_table(cx, "books.csv", "books",
                   ["book_id", "title", "author", "year", "description"])
        load_table(cx, "book_subjects.csv", "book_subjects", ["book_id", "subject_id"])
        load_table(cx, "book_views.csv", "book_views",
                   ["view_id", "book_id", "student_id", "career", "viewed_at"])
        load_table(cx, "search_events.csv", "search_events",
                   ["event_id", "student_id", "query", "filter_used", "clicked", "searched_at"])
        load_table(cx, "sessions.csv", "sessions",
                   ["session_id", "student_id", "started_at", "ended_at",
                    "duration_minutes", "books_browsed", "saved_final"])
        load_table(cx, "session_subjects.csv", "session_subjects", ["session_id", "subject_id"])
        load_table(cx, "saved_books.csv", "saved_books",
                   ["save_id", "student_id", "book_id", "browsing_depth_at_save", "saved_at"])
        cx.close()
        print("\n✅ All data loaded into the database.")
    except Exception as e:
        print(f"[ERROR] {e}")
        print("Check that PostgreSQL is running, schema is applied, and .env is set.")