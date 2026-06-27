# ============================================================
#  TeamX Digital Library — Real Books (hardcoded from Open Library)
#  Author: Roselyn G. Polanco González (2309184)
#
#  80 real books (10 per subject) sourced from Open Library.
#  No internet required — data is embedded directly.
#
#  Usage: python scripts/fetch_real_books.py
# ============================================================

import csv
import json
import os
from collections import Counter

BASE     = os.path.dirname(os.path.abspath(__file__))
CSV_DIR  = os.path.abspath(os.path.join(BASE, "../data/csv"))
JSON_DIR = os.path.abspath(os.path.join(BASE, "../data/json"))

REAL_BOOKS = [
    # Mathematics
    {"title": "Calculus",                                          "author": "Michael Spivak",          "year": 1967, "subject": "Mathematics"},
    {"title": "Introduction to Linear Algebra",                    "author": "Gilbert Strang",          "year": 1993, "subject": "Mathematics"},
    {"title": "Discrete Mathematics and Its Applications",         "author": "Kenneth H. Rosen",        "year": 1988, "subject": "Mathematics"},
    {"title": "Principles of Mathematical Analysis",               "author": "Walter Rudin",            "year": 1953, "subject": "Mathematics"},
    {"title": "Abstract Algebra",                                  "author": "David S. Dummit",         "year": 1991, "subject": "Mathematics"},
    {"title": "Linear Algebra Done Right",                         "author": "Sheldon Axler",           "year": 1995, "subject": "Mathematics"},
    {"title": "Topology",                                          "author": "James R. Munkres",        "year": 1975, "subject": "Mathematics"},
    {"title": "Numerical Analysis",                                "author": "Richard L. Burden",       "year": 1978, "subject": "Mathematics"},
    {"title": "A First Course in Probability",                     "author": "Sheldon Ross",            "year": 1976, "subject": "Mathematics"},
    {"title": "Mathematical Methods for Physics and Engineering",  "author": "K. F. Riley",             "year": 1997, "subject": "Mathematics"},
    # Programming
    {"title": "The C Programming Language",                        "author": "Brian W. Kernighan",      "year": 1978, "subject": "Programming"},
    {"title": "Structure and Interpretation of Computer Programs", "author": "Harold Abelson",          "year": 1984, "subject": "Programming"},
    {"title": "Clean Code",                                        "author": "Robert C. Martin",        "year": 2008, "subject": "Programming"},
    {"title": "The Pragmatic Programmer",                          "author": "Andrew Hunt",             "year": 1999, "subject": "Programming"},
    {"title": "Introduction to Algorithms",                        "author": "Thomas H. Cormen",        "year": 1990, "subject": "Programming"},
    {"title": "Design Patterns",                                   "author": "Erich Gamma",             "year": 1994, "subject": "Programming"},
    {"title": "Code Complete",                                     "author": "Steve McConnell",         "year": 1993, "subject": "Programming"},
    {"title": "Python Crash Course",                               "author": "Eric Matthes",            "year": 2015, "subject": "Programming"},
    {"title": "Eloquent JavaScript",                               "author": "Marijn Haverbeke",        "year": 2011, "subject": "Programming"},
    {"title": "Refactoring",                                       "author": "Martin Fowler",           "year": 1999, "subject": "Programming"},
    # Databases
    {"title": "Database System Concepts",                          "author": "Abraham Silberschatz",    "year": 1991, "subject": "Databases"},
    {"title": "An Introduction to Database Systems",               "author": "C. J. Date",              "year": 1975, "subject": "Databases"},
    {"title": "Fundamentals of Database Systems",                  "author": "Ramez Elmasri",           "year": 1989, "subject": "Databases"},
    {"title": "The Data Warehouse Toolkit",                        "author": "Ralph Kimball",           "year": 1996, "subject": "Databases"},
    {"title": "SQL and Relational Theory",                         "author": "C. J. Date",              "year": 2009, "subject": "Databases"},
    {"title": "NoSQL Distilled",                                   "author": "Pramod J. Sadalage",      "year": 2012, "subject": "Databases"},
    {"title": "Designing Data-Intensive Applications",             "author": "Martin Kleppmann",        "year": 2017, "subject": "Databases"},
    {"title": "PostgreSQL: Up and Running",                        "author": "Regina Obe",              "year": 2012, "subject": "Databases"},
    {"title": "Learning SQL",                                      "author": "Alan Beaulieu",           "year": 2005, "subject": "Databases"},
    {"title": "High Performance MySQL",                            "author": "Baron Schwartz",          "year": 2004, "subject": "Databases"},
    # Statistics
    {"title": "The Art of Statistics",                             "author": "David Spiegelhalter",     "year": 2019, "subject": "Statistics"},
    {"title": "Statistical Inference",                             "author": "George Casella",          "year": 1990, "subject": "Statistics"},
    {"title": "An Introduction to Statistical Learning",           "author": "Gareth James",            "year": 2013, "subject": "Statistics"},
    {"title": "Bayesian Data Analysis",                            "author": "Andrew Gelman",           "year": 1995, "subject": "Statistics"},
    {"title": "Naked Statistics",                                  "author": "Charles Wheelan",         "year": 2013, "subject": "Statistics"},
    {"title": "Statistics",                                        "author": "David Freedman",          "year": 1978, "subject": "Statistics"},
    {"title": "Practical Statistics for Data Scientists",          "author": "Peter Bruce",             "year": 2017, "subject": "Statistics"},
    {"title": "The Elements of Statistical Learning",              "author": "Trevor Hastie",           "year": 2001, "subject": "Statistics"},
    {"title": "Probability Theory: The Logic of Science",          "author": "E. T. Jaynes",            "year": 2003, "subject": "Statistics"},
    {"title": "Think Stats",                                       "author": "Allen B. Downey",         "year": 2011, "subject": "Statistics"},
    # Electronics
    {"title": "The Art of Electronics",                            "author": "Paul Horowitz",           "year": 1980, "subject": "Electronics"},
    {"title": "Electronic Devices and Circuit Theory",             "author": "Robert L. Boylestad",     "year": 1972, "subject": "Electronics"},
    {"title": "Microelectronic Circuits",                          "author": "Adel S. Sedra",           "year": 1982, "subject": "Electronics"},
    {"title": "Fundamentals of Electric Circuits",                 "author": "Charles K. Alexander",    "year": 2000, "subject": "Electronics"},
    {"title": "Digital Design",                                    "author": "M. Morris Mano",          "year": 1984, "subject": "Electronics"},
    {"title": "Electric Circuits",                                 "author": "James W. Nilsson",        "year": 1983, "subject": "Electronics"},
    {"title": "Signal Processing First",                           "author": "James H. McClellan",      "year": 2003, "subject": "Electronics"},
    {"title": "Foundations of Analog and Digital Electronic Circuits", "author": "Agarwal & Lang",     "year": 2005, "subject": "Electronics"},
    {"title": "CMOS VLSI Design",                                  "author": "Neil H. E. Weste",        "year": 1985, "subject": "Electronics"},
    {"title": "Introduction to Electrodynamics",                   "author": "David J. Griffiths",      "year": 1981, "subject": "Electronics"},
    # Biology
    {"title": "Campbell Biology",                                  "author": "Jane B. Reece",           "year": 1987, "subject": "Biology"},
    {"title": "Molecular Biology of the Cell",                     "author": "Bruce Alberts",           "year": 1983, "subject": "Biology"},
    {"title": "The Selfish Gene",                                  "author": "Richard Dawkins",         "year": 1976, "subject": "Biology"},
    {"title": "Genetics: Analysis and Principles",                 "author": "Robert J. Brooker",       "year": 1999, "subject": "Biology"},
    {"title": "Biochemistry",                                      "author": "Jeremy M. Berg",          "year": 1975, "subject": "Biology"},
    {"title": "The Double Helix",                                  "author": "James D. Watson",         "year": 1968, "subject": "Biology"},
    {"title": "On the Origin of Species",                          "author": "Charles Darwin",          "year": 1859, "subject": "Biology"},
    {"title": "Lehninger Principles of Biochemistry",              "author": "David L. Nelson",         "year": 1982, "subject": "Biology"},
    {"title": "Human Physiology",                                  "author": "Dee Unglaub Silverthorn", "year": 1998, "subject": "Biology"},
    {"title": "Brock Biology of Microorganisms",                   "author": "Michael T. Madigan",      "year": 1970, "subject": "Biology"},
    # Machine Learning
    {"title": "Pattern Recognition and Machine Learning",          "author": "Christopher M. Bishop",   "year": 2006, "subject": "Machine Learning"},
    {"title": "Deep Learning",                                     "author": "Ian Goodfellow",          "year": 2016, "subject": "Machine Learning"},
    {"title": "Hands-On Machine Learning with Scikit-Learn",       "author": "Aurélien Géron",          "year": 2017, "subject": "Machine Learning"},
    {"title": "The Hundred-Page Machine Learning Book",            "author": "Andriy Burkov",           "year": 2019, "subject": "Machine Learning"},
    {"title": "Machine Learning: A Probabilistic Perspective",     "author": "Kevin P. Murphy",         "year": 2012, "subject": "Machine Learning"},
    {"title": "Reinforcement Learning",                            "author": "Richard S. Sutton",       "year": 1998, "subject": "Machine Learning"},
    {"title": "Natural Language Processing with Python",           "author": "Steven Bird",             "year": 2009, "subject": "Machine Learning"},
    {"title": "Neural Networks and Deep Learning",                 "author": "Michael Nielsen",         "year": 2015, "subject": "Machine Learning"},
    {"title": "Data Science from Scratch",                         "author": "Joel Grus",               "year": 2015, "subject": "Machine Learning"},
    {"title": "Python Machine Learning",                           "author": "Sebastian Raschka",       "year": 2015, "subject": "Machine Learning"},
    # Ethics
    {"title": "Ethics: Inventing Right and Wrong",                 "author": "J. L. Mackie",            "year": 1977, "subject": "Ethics"},
    {"title": "The Nicomachean Ethics",                            "author": "Aristotle",               "year": -350, "subject": "Ethics"},
    {"title": "Groundwork of the Metaphysics of Morals",           "author": "Immanuel Kant",           "year": 1785, "subject": "Ethics"},
    {"title": "Utilitarianism",                                    "author": "John Stuart Mill",        "year": 1863, "subject": "Ethics"},
    {"title": "A Theory of Justice",                               "author": "John Rawls",              "year": 1971, "subject": "Ethics"},
    {"title": "The Ethics of Artificial Intelligence",             "author": "Nick Bostrom",            "year": 2011, "subject": "Ethics"},
    {"title": "Weapons of Math Destruction",                       "author": "Cathy O'Neil",            "year": 2016, "subject": "Ethics"},
    {"title": "Race After Technology",                             "author": "Ruha Benjamin",           "year": 2019, "subject": "Ethics"},
    {"title": "Algorithms of Oppression",                          "author": "Safiya Umoja Noble",      "year": 2018, "subject": "Ethics"},
    {"title": "The Age of Surveillance Capitalism",                "author": "Shoshana Zuboff",         "year": 2019, "subject": "Ethics"},
]


def write_csv(name, rows, fields):
    path = os.path.join(CSV_DIR, name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"[CSV]  {name} — {len(rows)} rows")


def write_json(name, rows):
    path = os.path.join(JSON_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"[JSON] {name} — {len(rows)} records")


if __name__ == "__main__":
    print("=== TeamX Real Books Loader (Rous — 2309184) ===\n")

    subjects_path = os.path.join(CSV_DIR, "subjects.csv")
    with open(subjects_path, encoding="utf-8") as f:
        subjects = list(csv.DictReader(f))
    subject_id_of = {s["name"]: int(s["subject_id"]) for s in subjects}

    books         = []
    book_subjects = []

    for i, entry in enumerate(REAL_BOOKS, start=1):
        books.append({
            "book_id":     i,
            "title":       entry["title"],
            "author":      entry["author"],
            "year":        entry["year"],
            "description": f"Academic book on {entry['subject']}.",
        })
        book_subjects.append({
            "book_id":    i,
            "subject_id": subject_id_of[entry["subject"]],
        })

    counts = Counter(e["subject"] for e in REAL_BOOKS)
    for subj, n in counts.items():
        print(f"  [{subj:<20}] {n} books")

    print(f"\nTotal: {len(books)} books, {len(book_subjects)} subject links\n")

    write_csv("books.csv",         books,         ["book_id", "title", "author", "year", "description"])
    write_csv("book_subjects.csv", book_subjects, ["book_id", "subject_id"])
    write_json("books.json",       books)

    print("\n✅ Real books written to CSV and JSON.")
    print("   Next: python scripts/load_data.py")
