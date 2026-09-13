import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta, date
from app import create_app
from app.extensions import db
from app.models.user import User, Role, UserProfile, CompanyProfile
from app.models.internship import Category, Internship, MicroProject
from app.models.application import Application, ApplicationStatus, ApplicationStatusHistory, SavedInternship
from app.models.interview import InterviewSchedule
from app.models.academic import AcademicEvaluation
from app.models.system import Announcement, Notification

env = os.getenv("FLASK_ENV", "prod" if os.getenv("RENDER") or os.getenv("PORT") else "dev")
app = create_app(env)

def seed():
    with app.app_context():
        print("Ensuring database tables exist...")
        db.create_all()

        if User.query.filter_by(email="superadmin@teleportal.ai").first():
            print("Database already seeded. Skipping duplicate seeding.")
            return

        print("Seeding Categories...")
        cats = [
            Category(name="Software Engineering", slug="software-engineering", icon="code"),
            Category(name="AI & Machine Learning", slug="ai-machine-learning", icon="brain"),
            Category(name="Cloud & DevOps", slug="cloud-devops", icon="cloud"),
            Category(name="Full-Stack Web", slug="full-stack-web", icon="laptop"),
            Category(name="Data Analytics", slug="data-analytics", icon="chart-bar")
        ]
        db.session.add_all(cats)
        db.session.flush()

        print("Seeding Administrators...")
        super_admin = User(
            name="Super Administrator",
            email="superadmin@teleportal.ai",
            role=Role.SUPER_ADMIN,
            is_verified=True
        )
        super_admin.set_password("Admin@12345")

        admin = User(
            name="System Admin",
            email="admin@teleportal.ai",
            role=Role.ADMIN,
            is_verified=True
        )
        admin.set_password("Admin@12345")
        db.session.add_all([super_admin, admin])
        db.session.flush()

        print("Seeding Verified Companies...")
        c1 = User(name="Sundar Pichai (HR Team)", email="hr@nexusai.io", role=Role.COMPANY, is_verified=True)
        c1.set_password("Company@12345")
        db.session.add(c1)
        db.session.flush()
        cp1 = CompanyProfile(
            user_id=c1.id,
            company_name="Nexus Innovations AI",
            slug="nexus-innovations-ai",
            location="Bengaluru, Karnataka",
            industry="Artificial Intelligence",
            company_size="100-500",
            description="Nexus AI builds enterprise foundation models and automated agentic pipelines for global Fortune 500 partners.",
            website="https://nexusai.io",
            is_cin_verified=True,
            hr_contact_name="Aditi Rao",
            hr_contact_email="hr@nexusai.io"
        )
        db.session.add(cp1)

        c2 = User(name="Satya Nadella (Hiring)", email="careers@cloudscale.tech", role=Role.COMPANY, is_verified=True)
        c2.set_password("Company@12345")
        db.session.add(c2)
        db.session.flush()
        cp2 = CompanyProfile(
            user_id=c2.id,
            company_name="CloudScale Infrastructure",
            slug="cloudscale-infrastructure",
            location="Hyderabad, Telangana",
            industry="Cloud Computing",
            company_size="50-200",
            description="Leading multi-cloud orchestration and container security provider specializing in Kubernetes and distributed systems.",
            website="https://cloudscale.tech",
            is_cin_verified=True,
            hr_contact_name="Vikram Seth",
            hr_contact_email="careers@cloudscale.tech"
        )
        db.session.add(cp2)

        print("Seeding Students...")
        s1 = User(name="Adarsh Rai", email="adarsh@student.com", role=Role.STUDENT, phone="+91 9876543210", is_verified=True)
        s1.set_password("Student@12345")
        db.session.add(s1)
        db.session.flush()
        sp1 = UserProfile(
            user_id=s1.id,
            college="SRDT Institute of Technology",
            branch="Computer Science & Engineering",
            graduation_year="2026",
            cgpa=9.2,
            skills="Python, Flask, JavaScript, React, SQL, Docker, Machine Learning, Git",
            bio="Passionate full-stack & AI software engineer eager to build high-scale web platforms and generative AI agentic systems.",
            github_url="https://github.com/raiadarsh0510",
            linkedin_url="https://linkedin.com/in/adarsh-rai",
            leetcode_url="https://leetcode.com",
            codeforces_url="https://codeforces.com"
        )
        db.session.add(sp1)

        s2 = User(name="Priya Sharma", email="priya@student.com", role=Role.STUDENT, is_verified=True)
        s2.set_password("Student@12345")
        db.session.add(s2)
        db.session.flush()
        sp2 = UserProfile(
            user_id=s2.id,
            college="National Institute of Technology",
            branch="Information Technology",
            graduation_year="2026",
            cgpa=8.9,
            skills="React, Tailwind CSS, TypeScript, UI/UX, Next.js, Figma",
            bio="Frontend specialist creating accessible, fluid user interfaces."
        )
        db.session.add(sp2)

        print("Seeding High-Impact Internships...")
        i1 = Internship(
            company_id=c1.id,
            category_id=cats[1].id,
            title="Generative AI & LLM Systems Intern",
            slug="generative-ai-llm-systems-intern",
            internship_type="Virtual",
            experience_level="Fresher",
            location="Remote / Bengaluru",
            stipend_type="Fixed",
            stipend_amount=25000,
            duration_weeks=12,
            openings=3,
            description="Work directly with our applied AI research team to build multi-modal agentic workflows, prompt evaluation pipelines, and fine-tune open-weights models.",
            responsibilities="Design RAG pipelines, benchmark vector databases, implement structured function calling, and evaluate LLM hallucination rates.",
            requirements="Solid knowledge of Python, PyTorch or TensorFlow, familiarity with Hugging Face transformers, and REST APIs.",
            skills="Python, PyTorch, LLMs, LangChain, REST API, Git",
            benefits="PPO opportunity for high performers, 1-on-1 mentorship from principal AI scientists, flexible hours.",
            deadline=date.today() + timedelta(days=45),
            is_active=True,
            is_featured=True,
            has_ppo_opportunity=True
        )

        i2 = Internship(
            company_id=c2.id,
            category_id=cats[0].id,
            title="Full Stack Software Engineer Intern",
            slug="full-stack-software-engineer-intern",
            internship_type="Hybrid",
            experience_level="Fresher",
            location="Hyderabad",
            stipend_type="Fixed",
            stipend_amount=20000,
            duration_weeks=10,
            openings=4,
            description="Collaborate with core backend engineers to design scalable RESTful services and build high-performance dashboard interfaces.",
            responsibilities="Develop microservices in Python/Flask, write unit and integration tests, optimize SQL queries, and implement responsive UI components.",
            requirements="Proficiency in Python or Node.js, relational databases (MySQL/PostgreSQL), and modern frontend frameworks.",
            skills="Python, Flask, SQL, React, Docker, Git",
            benefits="Certificate of Excellence, Letter of Recommendation, Pre-Placement Offer (PPO).",
            deadline=date.today() + timedelta(days=30),
            is_active=True,
            is_featured=True,
            has_ppo_opportunity=True
        )

        i3 = Internship(
            company_id=c2.id,
            category_id=cats[2].id,
            title="DevOps & Cloud Automation Intern",
            slug="devops-cloud-automation-intern",
            internship_type="Virtual",
            experience_level="Intermediate",
            location="Remote",
            stipend_type="Fixed",
            stipend_amount=18000,
            duration_weeks=8,
            openings=2,
            description="Implement CI/CD automation pipelines using GitHub Actions, Docker, and Kubernetes clusters.",
            responsibilities="Maintain Docker containers, write infrastructure-as-code scripts, monitor system uptime and telemetry metrics.",
            requirements="Familiarity with Linux command line, Docker containers, basic bash scripting.",
            skills="Docker, Linux, Kubernetes, CI/CD, AWS",
            benefits="Mentorship from AWS certified solutions architects, monthly learning allowance.",
            deadline=date.today() + timedelta(days=20),
            is_active=True,
            is_featured=False
        )

        db.session.add_all([i1, i2, i3])
        db.session.flush()

        print("Seeding Micro-Projects & Bounties...")
        mp1 = MicroProject(
            company_id=c1.id,
            title="Build an Interactive Resume ATS Scorer Widget",
            bounty_amount=5000,
            estimated_hours=15,
            skills_required="Python, Flask, NLP, HTML/CSS",
            deliverable_description="Create a standalone modular widget that accepts a resume text and calculates keyword density, readability index, and structural checklist.",
            submission_deadline=date.today() + timedelta(days=14)
        )
        mp2 = MicroProject(
            company_id=c2.id,
            title="Dockerize Multi-Service Flask & Redis Stack",
            bounty_amount=4000,
            estimated_hours=10,
            skills_required="Docker, Docker Compose, Nginx",
            deliverable_description="Write production-hardened Dockerfile and docker-compose configurations with multi-stage builds and health check probes.",
            submission_deadline=date.today() + timedelta(days=10)
        )
        db.session.add_all([mp1, mp2])
        db.session.flush()

        print("Seeding Applications...")
        app1 = Application(
            internship_id=i1.id,
            student_id=s1.id,
            status=ApplicationStatus.SHORTLISTED,
            match_score=92,
            cover_letter="I am thrilled to apply for the Generative AI Intern role. With my background in Python and LLM prompt engineering, I look forward to contributing immediately."
        )
        app2 = Application(
            internship_id=i2.id,
            student_id=s1.id,
            status=ApplicationStatus.INTERVIEW_SCHEDULED,
            match_score=88,
            cover_letter="Full-stack engineering is my primary domain of expertise. I have built production Flask applications with MySQL and Docker."
        )
        db.session.add_all([app1, app2])
        db.session.flush()

        print("Seeding Interview Schedule...")
        interview1 = InterviewSchedule(
            application_id=app2.id,
            company_id=c2.id,
            student_id=s1.id,
            interview_type="Technical Round",
            meeting_link="https://meet.google.com/abc-defg-hij",
            scheduled_at=datetime.utcnow() + timedelta(days=2, hours=3),
            duration_minutes=45,
            status="scheduled"
        )
        db.session.add(interview1)

        print("Seeding Academic Evaluation (NEP 2020)...")
        eval1 = AcademicEvaluation(
            application_id=app1.id,
            student_id=s1.id,
            company_id=c1.id,
            college_name="SRDT Institute of Technology",
            faculty_mentor_name="Dr. K. S. Sharma",
            faculty_mentor_email="mentor@srdt.ac.in",
            attendance_percentage=98.5,
            technical_competence=5,
            professionalism=5,
            project_completion=5,
            overall_performance=9.8,
            nep_credits_awarded=4,
            grade="O",
            company_remarks="Adarsh displayed exemplary engineering discipline, autonomous problem solving, and delivered features ahead of schedule.",
            is_verified_by_college=True,
            verified_at=datetime.utcnow()
        )
        db.session.add(eval1)

        print("Seeding Announcements & Notifications...")
        ann = Announcement(
            title="Welcome to TELEPORTAL National Launch",
            content="TELEPORTAL is now live with AI-powered resume scoring, micro-internship bounties, and official NEP 2020 academic credit transfer.",
            target_role="all"
        )
        notif = Notification(
            user_id=s1.id,
            title="Interview Scheduled with CloudScale!",
            message="Your technical interview for 'Full Stack Software Engineer Intern' has been scheduled.",
            link="/student/dashboard"
        )
        db.session.add_all([ann, notif])

        db.session.commit()
        print("DATABASE SEEDING COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    seed()