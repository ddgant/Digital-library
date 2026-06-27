<div align="center">

# TeamX — Digital Library Platform

### A digital library platform where students can search, browse, and save academic books — instrumented to support five behavioral research questions.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-API-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#license)

[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](#)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](#)

</div>

<br>

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4169E1,100:3776AB&height=120&section=header&text=&fontSize=0" width="100%"/>
</div>

---

## Table of Contents

- [Repository Structure](#repository-structure)
- [Research Questions](#research-questions)
- [How to Run Locally](#how-to-run-locally)
- [Database Schema Overview](#database-schema-overview)
- [API Endpoints](#api-endpoints)
- [Sample Data](#sample-data)
- [Team Members & Roles](#team-members--roles)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## Repository Structure

```
digital-library/
├── database/                  # Schema SQL (Mauricio)
│   └── schema.sql
├── api/                       # REST API with Flask (Rodrigo)
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── books.py           # Catalog + view logging
│   │   ├── search.py          # Search + click tracking
│   │   ├── sessions.py        # Sessions, browsing depth, subjects
│   │   ├── saves.py           # Saved books
│   │   └── subjects.py        # Subject traffic by career
│   ├── middleware/
│   │   └── auth.py
│   └── controllers/
│       └── base.py
├── frontend/                  # HTML forms and UI (Arturo)
│   ├── index.html
│   ├── forms/
│   │   ├── search_form.html
│   │   ├── book_form.html
│   │   └── saved_form.html
│   └── static/
│       └── style.css
├── data/                      # Generated sample data (Rous)
│   ├── csv/                   # 9 CSV files
│   ├── json/                  # 4 JSON files
│   └── excel/
│       └── library_analytics.xlsx
├── scripts/                   # Data generation & loaders (Rous)
│   ├── generate_data.py
│   ├── fetch_real_books.py    # Loads 80 real books (Open Library)
│   └── load_data.py
├── .github/workflows/
│   └── deploy.yml             # GitHub Actions CI/CD
└── README.md                  # Documentation (Diego)
```

---

## Research Questions

The platform is instrumented so each member can extract data for their question:

| Member | Research Question | Statistical Indicator | Data Source |
|--------|-------------------|-----------------------|-------------|
| **Arturo** | Do students who apply a subject filter before searching have a higher search-to-click conversion rate? | Conversion rate as a proportion between both groups | `search_events` |
| **Diego** | Is there a subject area that receives consistent traffic across all four career programs? | Proportion of views per subject by career (evenness ratio) | `book_views`, `book_subjects` |
| **Rous** | Do books tagged with more than one subject receive more detail page views on average? | Mean view count: single-tagged vs. multi-tagged | `books`, `book_subjects`, `book_views` |
| **Rodrigo** | Do students who browse more books before choosing have a higher probability of saving? | Correlation between browsing depth and save probability | `sessions`, `saved_books` |
| **Mauricio** | Is there a relationship between session duration and number of distinct subjects visited? | Pearson correlation between duration and subject count | `sessions`, `session_subjects` |

---

## How to Run Locally

### Prerequisites
- Python 3.10+
- PostgreSQL 14+

### 1. Clone the repository
```bash
git clone https://github.com/ddgant/digital-library.git
cd digital-library
```

### 2. Install dependencies
```bash
pip install -r api/requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Create the database and apply the schema
```bash
psql -U postgres -c "CREATE DATABASE teamx_library;"
psql -U postgres -d teamx_library -f database/schema.sql
```

### 5. Generate and load the sample data
```bash
python scripts/generate_data.py     # writes CSV / JSON / Excel into data/
python scripts/fetch_real_books.py  # replaces books with 80 real titles
python scripts/load_data.py         # loads the CSVs into PostgreSQL
```

### 6. Run the API server
```bash
cd api
python app.py
```
> API available at `http://localhost:5000` — test with `GET /api/health`

### 7. Open the frontend
```bash
python -m http.server 8080 --directory frontend
# then open http://localhost:8080
```

---

## Database Schema Overview

| Table | Description |
|-------|-------------|
| `students` | Student profiles with **career affiliation** and semester |
| `books` | Book catalog (title, author, year, description) |
| `subjects` | Subject areas / tags |
| `book_subjects` | Many-to-many book ↔ subject relationship |
| `book_views` | Detail-page view events (with career) |
| `search_events` | Search queries with `filter_used` and `clicked` flags |
| `sessions` | Sessions with duration, browsing depth, final-save flag |
| `session_subjects` | Distinct subjects visited per session |
| `saved_books` | Saved books with browsing depth recorded at save time |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| 🟢 `GET`  | `/api/health` | Health check |
| 🟢 `GET`  | `/api/books` | List books (optional `?subject=`) |
| 🟢 `GET`  | `/api/books/<id>` | Get book detail + log a view |
| 🟡 `POST` | `/api/books` | Add a new book |
| 🟢 `GET`  | `/api/search?q=&filter_used=` | Search books, logs filter usage |
| 🟡 `POST` | `/api/search/click` | Register a result click (conversion) |
| 🟡 `POST` | `/api/sessions` | Start a session |
| 🔵 `PUT`  | `/api/sessions/<id>/end` | End a session (computes duration) |
| 🟡 `POST` | `/api/sessions/<id>/subjects` | Log a subject visited |
| 🟡 `POST` | `/api/sessions/<id>/browse` | Increment browsing depth |
| 🟢 `GET`  | `/api/saves?student_id=` | List a student's saved books |
| 🟡 `POST` | `/api/saves` | Save a book |
| 🟢 `GET`  | `/api/subjects` | List all subjects |
| 🟢 `GET`  | `/api/subjects/<id>/stats` | Subject views broken down by career |

---

## Sample Data

Generated by `scripts/generate_data.py` (fixed seed → reproducible), with the
book catalog replaced by 80 real titles via `scripts/fetch_real_books.py`:

| Dataset | Rows | Formats |
|---------|------|---------|
| students | 200 | CSV, JSON |
| books | 80 | CSV, JSON |
| subjects | 8 | CSV, JSON |
| book_subjects | 80 | CSV |
| book_views | 5,000 | CSV, JSON |
| search_events | 1,500 | CSV |
| sessions | 800 | CSV |
| session_subjects | ~2,800 | CSV |
| saved_books | ~430 | CSV |

The Excel workbook `data/excel/library_analytics.xlsx` contains three summary
sheets (book tag summary, session stats, search conversion) for quick inspection.

---

## Team Members & Roles

<div align="center">

| Name | ID | Role | Contribution |
|------|----|------|--------------|
| **Mauricio Gabriel Ramírez Rubio** | 2309192 | Database Design | `database/schema.sql` |
| **Rodrigo García Martínez** | 2309091 | API Design | `api/` — Flask routes, controllers, middleware |
| **Cesar Arturo Balam Euan** | 2309017 | Frontend & Form Design | `frontend/` — HTML forms and CSS |
| **Roselyn G. Polanco González** | 2309184 | Data Generation & Instrumentation | `data/`, `scripts/` |
| **Diego De Gante Pérez** | 2309067 | Documentation | `README.md`, API docs, inline comments |
| **Dr. Jorge J. Pedrozo Romero** | — | Course Professor | Project supervision and guidance |

</div>

---

## Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Backend-Python%20%2F%20Flask-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/Frontend-HTML5%20%2F%20CSS3-E34F26?style=flat-square&logo=html5&logoColor=white)
![Excel](https://img.shields.io/badge/Data-CSV%20%2F%20JSON%20%2F%20Excel-217346?style=flat-square&logo=microsoftexcel&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Git](https://img.shields.io/badge/Version%20Control-Git%20%2F%20GitHub-F05032?style=flat-square&logo=git&logoColor=white)

</div>

---

## License

<div align="center">

**MIT License** — TeamX, 2025

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:3776AB,100:4169E1&height=100&section=footer" width="100%"/>

</div>
