# TELEPORTAL Entity Relationship Diagram (ERD)

The following diagram illustrates the relational data model of TELEPORTAL, capturing all 15 core entities, foreign key dependencies, and cardinalities.

```mermaid
erDiagram
    USERS ||--o| USER_PROFILES : "has one"
    USERS ||--o| COMPANY_PROFILES : "has one"
    USERS ||--o{ INTERNSHIPS : "posts"
    USERS ||--o{ APPLICATIONS : "submits"
    USERS ||--o{ NOTIFICATIONS : "receives"
    USERS ||--o{ AUDIT_LOGS : "triggers"
    USERS ||--o{ INTERVIEW_SCHEDULES : "participates"
    USERS ||--o{ RESUME_ANALYSES : "conducts"
    USERS ||--o{ MOCK_INTERVIEW_SESSIONS : "attempts"

    CATEGORIES ||--o{ INTERNSHIPS : "classifies"
    
    INTERNSHIPS ||--o{ APPLICATIONS : "receives"
    INTERNSHIPS ||--o{ SAVED_INTERNSHIPS : "saved by"
    INTERNSHIPS ||--o{ MICRO_PROJECTS : "associates"

    APPLICATIONS ||--o{ APPLICATION_STATUS_HISTORY : "tracks"
    APPLICATIONS ||--o{ INTERVIEW_SCHEDULES : "schedules"
    APPLICATIONS ||--o| ACADEMIC_EVALUATIONS : "evaluated as"

    MICRO_PROJECTS ||--o{ MICRO_SUBMISSIONS : "receives"
    USERS ||--o{ MICRO_SUBMISSIONS : "solves"

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        string phone
        boolean is_active
        boolean is_verified
        datetime created_at
        datetime last_login
    }

    USER_PROFILES {
        int id PK
        int user_id FK
        string college
        string branch
        string graduation_year
        float cgpa
        text skills
        text bio
        string github_url
        string linkedin_url
        string leetcode_url
    }

    COMPANY_PROFILES {
        int id PK
        int user_id FK
        string company_name
        string website
        string industry
        string location
        text description
    }

    CATEGORIES {
        int id PK
        string name UK
        string slug UK
        string icon
    }

    INTERNSHIPS {
        int id PK
        string title
        string slug UK
        int company_id FK
        int category_id FK
        string internship_type
        string experience_level
        string location
        string stipend_type
        int stipend_amount
        int duration_weeks
        text requirements
        string skills
        date deadline
        boolean is_active
    }

    APPLICATIONS {
        int id PK
        int internship_id FK
        int student_id FK
        string status
        int match_score
        text cover_letter
        datetime applied_at
    }

    ACADEMIC_EVALUATIONS {
        int id PK
        int application_id FK
        int student_id FK
        int company_id FK
        string college_name
        float attendance_percentage
        int technical_competence
        int professionalism
        int project_completion
        float overall_performance
        int nep_credits_awarded
        string grade
        boolean is_verified_by_college
    }

    INTERVIEW_SCHEDULES {
        int id PK
        int application_id FK
        int company_id FK
        int student_id FK
        string interview_type
        string meeting_link
        datetime scheduled_at
        string status
    }

    MICRO_PROJECTS {
        int id PK
        int company_id FK
        string title
        text description
        string bounty_amount
        string skills_required
        boolean is_active
    }

    MICRO_SUBMISSIONS {
        int id PK
        int project_id FK
        int student_id FK
        string submission_url
        string github_pr_url
        string status
    }

    AUDIT_LOGS {
        int id PK
        int user_id FK
        string action
        string entity_type
        int entity_id
        string ip_address
        string details
        datetime created_at
    }

    ANNOUNCEMENTS {
        int id PK
        string title
        text content
        string target_role
        datetime created_at
    }
```