<div align="center">

# TeamX — Digital Library Platform

### A digital library platform where students can search, browse, and save academic books — built to support behavioral data research.

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
- [Team Members & Roles](#team-members--roles)
- [Tech Stack](#tech-stack)
- [License](#license)

---

## Repository Structure

```
digital-library/
├── database/                  # Schema SQL + seed data (Mauricio)
│   └── schema.sql
├── api/                       # REST API skeleton (Rodrigo)
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── books.py           # Book catalog endpoints
│   │   ├── search.py          # Search + click tracking
│   │   ├── sessions.py        # Session & browsing depth
│   │   ├── saves.py           # Saved books
│   │   └── subjects.py        # Subject traffic stats
│   ├── middleware/
│   │   └── auth.py
│   └── controllers/
│       └── base.py
├── frontend/                  # HTML forms and UI (Arturo)
│   ├── index.html
│   ├── forms/
│   │   ├── search_form.html   # Search with filter toggle
│   │   ├── book_form.html     # Book detail + save button
│   │   └── saved_form.html    # Student's saved books
│   └── static/
│       └── style.css
├── data/                      # Sample datasets (Rous)
│   ├── csv/
│   ├── json/
│   └── excel/
├── scripts/                   # Data generation scripts (Rous)
│   ├── generate_data.py
│   └── load_data.py
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions CI/CD
└── README.md
```

---

## Research Questions

| Member | Question | Statistical Indicator |
|--------|----------|-----------------------|
| **Arturo** | Do students who apply a subject filter before searching have a higher search-to-click conversion rate? | Conversion rate as a proportion, compared between both groups |
| **Diego** | Is there a subject area that receives consistent traffic from students across all four career programs? | Proportion of views per subject broken down by career affiliation |
| **Rous** | Do books tagged with more than one subject receive more detail page views on average? | Mean view count compared between single-tagged and multi-tagged books |
| **Rodrigo** | Do students who browse more books before choosing one have a higher probability of saving? | Correlation between browsing depth and save probability |
| **Mauricio** | Is there a relationship between total session duration and the number of distinct subjects visited? | Pearson correlation between session duration and subject count |

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

### 2. Set up the database
```bash
psql -U postgres -c "CREATE DATABASE teamx_library;"
psql -U postgres -d teamx_library -f database/schema.sql
```

### 3. Install API dependencies
```bash
cd api
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your DB credentials
```

### 5. Run the API server
```bash
cd api
python app.py
```
> API will be available at `http://localhost:5000`

### 6. Open the frontend
```bash
open frontend/index.html
# Or serve it:
python -m http.server 8080 --directory frontend
```

### 7. Generate and load sample data
```bash
cd scripts
python generate_data.py   # Creates CSV/JSON/Excel files
python load_data.py       # Loads data into the database
```

---

## Database Schema Overview

| Table              | Description                                               |
|--------------------|-----------------------------------------------------------|
| `students`         | Student profiles, career affiliation, and semester        |
| `books`            | Book catalog with title, author, and description          |
| `book_subjects`    | Many-to-many relation between books and subject tags      |
| `book_views`       | Detail page view events per student                       |
| `search_events`    | Search queries with filter usage and click tracking       |
| `sessions`         | Student sessions with duration and browsing depth         |
| `session_subjects` | Subjects visited within each session                      |
| `saved_books`      | Books saved by students, with browsing depth at save time |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| 🟢 `GET`  | `/api/books` | List all books |
| 🟡 `POST` | `/api/books` | Add a new book |
| 🟢 `GET`  | `/api/books/<id>` | Get book detail + log view |
| 🟢 `GET`  | `/api/search` | Search books (logs filter usage) |
| 🟡 `POST` | `/api/search/click` | Register a search result click |
| 🟡 `POST` | `/api/sessions` | Start a session |
| 🔵 `PUT`  | `/api/sessions/<id>/end` | End a session |
| 🟡 `POST` | `/api/sessions/<id>/subjects` | Log a subject visit |
| 🟡 `POST` | `/api/sessions/<id>/browse` | Increment browsing depth |
| 🟢 `GET`  | `/api/saves` | List saved books for a student |
| 🟡 `POST` | `/api/saves` | Save a book |
| 🟢 `GET`  | `/api/subjects` | List subjects with traffic stats |
| 🟢 `GET`  | `/api/subjects/<id>/stats` | Subject views broken down by career |

---

## Team Members & Roles

<div align="center">

| Name | ID | Role | Contribution |
|------|----|------|--------------|
| **Mauricio Gabriel Ramírez Rubio** | 2309192 | Database Design | `database/schema.sql` |
| **Rodrigo García Martínez** | 2309091 | API Design | `api/` — Flask routes, controllers, middleware |
| **Cesar Arturo Balam Euan** | 2309017 | Frontend & Form Design | `frontend/` — HTML forms and CSS styles |
| **Roselyn G. Polanco González** | 2309184 | Data Generation & Instrumentation | `data/`, `scripts/` — sample datasets and loaders |
| **Diego De Gante Pérez** | 2309067 | Documentation | `README.md`, inline code comments, API docs |
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
