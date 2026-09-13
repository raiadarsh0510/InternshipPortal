<div align="center">

# 🚀 TELEPORTAL
### *A Next Generation AI-Powered Internship Management & Career Acceleration Platform*

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-32%20passed%20(100%25)-brightgreen.svg)]()
[![NEP 2020](https://img.shields.io/badge/compliance-NEP%202020%20ABC-orange.svg)]()
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg?logo=docker&logoColor=white)]()

<p align="center">
  TELEPORTAL is an enterprise-grade internship management platform engineered from the ground up to solve systemic gaps in traditional hiring: the "experience paradox", ghosting/slow review cycles, ATS incompatibility, and the lack of academic credit integration.
</p>

</div>

---

## 🌟 Visual Showcase

<div align="center">
  <img width="828" alt="TELEPORTAL UI" src="https://github.com/user-attachments/assets/e48b66d2-ca5b-4b40-b227-54e19b3fe99f" />
  <br/><br/>
  <img width="887" alt="Dashboard" src="https://github.com/user-attachments/assets/b5bc6f75-ff32-422a-81a2-4a19f5558acf" />
  <br/><br/>
  <img width="798" alt="Applicant Pipeline" src="https://github.com/user-attachments/assets/64d44837-631a-4515-abe7-c79fdd63d790" />
</div>

---

## 🎯 Groundbreaking Gap-Filling Solutions

| Traditional Platform Limitation | TELEPORTAL Innovation |
| :--- | :--- |
| **Experience Paradox**: Students have no prior experience to land entry-level internships. | **Micro-Internship Bounties**: Complete bite-sized, real corporate proof-of-work tasks to earn verified badges and fast-track interviews. |
| **Recruiter Ghosting & Slow Cycles**: Applicants wait months with zero feedback. | **Recruiter Review SLAs**: Mandatory 48h to 72h review windows with automated candidate status tracking. |
| **Resume Black Holes & ATS Rejection**: Resumes get filtered before human eyes see them. | **AI ATS Optimizer & Tailored Cover Letter Builder**: Instant ATS scoring, missing keyword detection, and customized application letters. |
| **Disconnected Academic Transcripts**: Internships are rarely mapped to college degrees. | **NEP 2020 Academic Credit Rubric**: University mentor evaluation directly maps internship performance into the Academic Bank of Credits (ABC). |
| **Nerve-Wracking Interviews**: Students lack targeted preparation. | **AI Mock Interview Simulator**: Voice/text dictation simulator providing STAR feedback, clarity metrics, and scoring. |

---

## 🏗️ Architecture & Tech Stack

```
TELEPORTAL/
├── app/
│   ├── models/            # 15 Normalized SQLAlchemy Relational Models
│   ├── routes/            # Decoupled Blueprints (Auth, Student, Company, Admin, Internship, AI, API)
│   ├── services/          # Pure Business Logic (AI Engine, Application, Internship, Academic, Security)
│   ├── repositories/      # Data Access Layer & Advanced Query Filtering
│   ├── forms/             # WTForms with Strict Validation & CSRF Protection
│   ├── extensions.py      # Extension Registry (DB, Migrate, Login, Limiter, CSRF, Mail)
│   └── __init__.py        # Enterprise Application Factory (`create_app`)
├── docker/                # Multi-stage Dockerfile, docker-compose.yml, nginx.conf
├── docs/                  # Architecture, REST API, ERD Diagram, and User Manual
├── seeds/                 # Comprehensive Multi-Role Database Seeder
├── static/                # Modern Glassmorphism CSS, Vanilla ES6 JS, Uploads
├── templates/             # Bootstrap 5 + Glassmorphism Jinja2 Views
│   ├── admin/             # Governance, User Moderation, Audit Logs, Announcements
│   ├── ai/                # ATS Analyzer, Mock Interview, Skill Gap, Cover Letter
│   ├── auth/              # Dual Role Registration & Secure Authentication
│   ├── company/           # Employer Job Poster, Pipeline Manager, NEP Evaluation
│   ├── errors/            # Custom 404, 500, 403, 429 Glassmorphic Error Pages
│   ├── internship/        # Discovery Board, Detail View, Micro-Bounties
│   └── student/           # Dashboard, Profile, Applications, Saved, NEP Credits
├── tests/                 # 32 Automated Unit & Integration Tests (Pytest)
├── config.py              # Environment Configurations (Dev, Prod, Test)
├── wsgi.py / run.py       # Production WSGI & Development Entrypoints
└── requirements.txt       # Frozen Production Dependencies
```

### Technology Stack
- **Backend Core**: Python 3.12+, Flask 3.0+, SQLAlchemy ORM, Alembic, Flask-Login, Flask-WTF, Flask-Limiter.
- **Frontend Architecture**: HTML5, Modern Glassmorphism CSS3, Bootstrap 5.3, Bootstrap Icons, Chart.js, ES6 JavaScript, Web Speech Recognition.
- **Database**: MySQL 8.0 / PostgreSQL with auto-fallback to SQLite for seamless local prototyping.
- **AI Engine**: Multi-provider generative AI (OpenAI GPT / Gemini) with an intelligent zero-cost heuristic NLP fallback.
- **Deployment & DevOps**: Docker, Docker Compose, Nginx Reverse Proxy, Gunicorn, GitHub Actions CI/CD.

---

## ⚡ Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/raiadarsh0510/InternshipPortal.git
cd InternshipPortal
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
Populates Super Admin, Admin, verified employers, students, sample internships, and NEP evaluations:
```bash
python seeds/seed_data.py
```

### 5. Run the Application
```bash
python run.py
```
Open **`http://localhost:5000`** in your browser.

---

## 🔑 Default Credentials (Seed Data)

| Role | Email | Password | Clearances |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `superadmin@teleportal.ai` | `Admin@123` | Full system governance, audit logs, user suspension |
| **Admin** | `admin@teleportal.ai` | `Admin@123` | Listing moderation, user management, announcements |
| **Company 1** | `hr@nexusai.com` | `Company@123` | Post internships, manage applicants, NEP grading |
| **Company 2** | `talent@cloudscale.io` | `Company@123` | Micro-bounties, interview scheduling |
| **Student 1** | `adarsh@university.edu` | `Student@123` | Applications, ATS scoring, mock interviews, NEP credits |
| **Student 2** | `priya@technology.ac.in` | `Student@123` | Candidate profile, portfolio links, bounties |

---

## 🐳 Docker Deployment

Run the complete multi-container stack (Flask + MySQL 8 + Redis 7 + Nginx):

```bash
cd docker
docker-compose up --build -d
```
Access the application on port `80`: **`http://localhost`**.

---

## 🧪 Running Automated Tests

TELEPORTAL includes 32 automated tests covering authentication, application pipelines, recruiter moderation, NEP credit evaluation, and AI services:

```bash
pytest tests/ -v
```

---

## 📖 In-Depth Documentation

- 🏛️ [System Architecture & Design Patterns](docs/ARCHITECTURE.md)
- 🔌 [REST API Endpoints & Payload Specifications](docs/API_DOCUMENTATION.md)
- 📊 [Entity-Relationship Diagram (ERD)](docs/ER_DIAGRAM.md)
- 📘 [Role-Based User Manual & Step-by-Step Guides](docs/USER_MANUAL.md)

---

## 👨‍💻 Author & Maintainer

Developed by **[Adarsh Rai](https://github.com/raiadarsh0510)**.
Contributions, issues, and feature requests are welcome!