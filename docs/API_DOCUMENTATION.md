# TELEPORTAL REST API Specification (v2.0)

## 1. Overview & Authentication
TELEPORTAL exposes RESTful endpoints supporting JSON payloads. Session cookies and CSRF tokens protect interactive web routes, while JSON API routes accept standard headers.

**Base URL**: `http://localhost:5000/api/v1` or `/api`

---

## 2. Authentication & User Endpoints

### `POST /login`
Authenticates user credentials and establishes a secure session.
- **Request**:
  ```json
  {
    "email": "student@test.com",
    "password": "Password123",
    "remember": true
  }
  ```
- **Response (302 Redirect)**: Redirects to role dashboard (`/student/dashboard`, `/company/dashboard`, or `/admin/dashboard`).

### `POST /register?role={student|company}`
Registers a new platform user.
- **Student Payload**:
  `name`, `email`, `password`, `confirm_password`, `phone`, `college`, `branch`
- **Company Payload**:
  `company_name`, `hr_name`, `email`, `password`, `confirm_password`, `location`, `website`

---

## 3. Internship & Bounty Endpoints

### `GET /internships`
Fetches paginated list of active opportunities with multi-parameter filtering.
- **Query Parameters**:
  - `q`: Search keyword (title, company, skills)
  - `category`: Category ID integer
  - `location`: City or region
  - `type`: `Virtual`, `On-site`, or `Hybrid`
  - `min_stipend`: Minimum monthly stipend in INR
  - `remote`: `true` or `false`
  - `page`: Page number (default: 1)

### `GET /internship/<id>`
Retrieves full details for a specific internship posting.

### `POST /internship/<id>/apply`
Submits an application on behalf of the authenticated student.
- **Form Data**:
  - `cover_letter`: Text
  - `resume_path`: Optional file path override

### `POST /internship/<id>/save-toggle`
Saves or unsaves an internship for the student.
- **Response**:
  ```json
  {
    "success": true,
    "saved": true
  }
  ```

### `GET /micro-bounties`
Retrieves proof-of-work micro-internship bounties.

### `POST /micro-bounties/<id>/submit`
Submits proof-of-work repository URL, pull request link, and notes.

---

## 4. Employer Management Endpoints

### `POST /company/post-internship`
Publishes a new internship listing.
- **Payload**:
  - `title`: String
  - `category_id`: Integer
  - `internship_type`: `Virtual` | `On-site` | `Hybrid`
  - `location`: String
  - `stipend_type`: `Fixed` | `Performance` | `Unpaid`
  - `stipend_amount`: Integer
  - `duration_weeks`: Integer
  - `openings`: Integer
  - `skills`: Comma-separated string
  - `description`: Text
  - `deadline`: Date (`YYYY-MM-DD`)

### `GET /company/applicants/<internship_id>`
Returns all candidates for the given internship sorted by AI match score.

### `POST /company/application/<application_id>/status`
Transitions application state.
- **Payload**:
  - `status`: `applied` | `under_review` | `shortlisted` | `interview_scheduled` | `accepted` | `rejected`
  - `comment`: Optional recruiter note

### `POST /company/evaluate/<application_id>`
Submits NEP 2020 composite credit evaluation.
- **Payload**:
  - `attendance`: Float (percentage)
  - `tech_comp`: Integer (1-5)
  - `professionalism`: Integer (1-5)
  - `proj_comp`: Integer (1-5)
  - `faculty_mentor_name`: String
  - `faculty_mentor_email`: Email
  - `remarks`: Text

---

## 5. AI Engine Endpoints

### `POST /ai/resume-analyzer`
Analyzes resume text against target role expectations.
- **Payload**:
  - `resume_text`: String (min 50 characters)
  - `target_role`: String
- **Response**:
  ```json
  {
    "ats_score": 85,
    "readability_score": 90,
    "found_skills": ["python", "flask", "docker", "sql"],
    "missing_skills": ["kubernetes"],
    "suggestions": ["Include quantifiable metrics"]
  }
  ```

### `POST /ai/mock-interview/evaluate`
Grades user interview response.
- **Payload**:
  - `question`: String
  - `answer`: String
  - `role`: String
- **Response**:
  ```json
  {
    "score": 8,
    "feedback": "Strong answer demonstrating good conceptual understanding...",
    "strengths": "Clear clarity, professional vocabulary...",
    "improvement": "Connect your explanation to measurable outcomes..."
  }
  ```

### `POST /api/v1/copilot-chat`
Inline AI Career Copilot conversation query.
- **Payload**:
  ```json
  { "message": "How do I optimize my resume?" }
  ```
- **Response**:
  ```json
  {
    "reply": "To optimize your resume for ATS, ensure your section headings are standard..."
  }
  ```