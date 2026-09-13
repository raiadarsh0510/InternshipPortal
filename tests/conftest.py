import pytest
from datetime import date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User, Role, UserProfile, CompanyProfile
from app.models.internship import Category, Internship

@pytest.fixture(scope="function")
def app():
    app = create_app("test")
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SERVER_NAME": "localhost"
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def student_user(app):
    user = User(
        name="Test Student",
        email="student@test.com",
        phone="+91 9876543210",
        role=Role.STUDENT,
        is_verified=True,
        is_active=True
    )
    user.set_password("StudentPass@123")
    db.session.add(user)
    db.session.commit()

    profile = UserProfile(
        user_id=user.id,
        college="Indian Institute of Technology",
        branch="Computer Science",
        graduation_year="2026",
        skills="Python, Flask, React, SQL, Docker",
        bio="Aspiring Software Engineer",
        github_url="https://github.com/teststudent",
        linkedin_url="https://linkedin.com/in/teststudent"
    )
    db.session.add(profile)
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def company_user(app):
    user = User(
        name="Test Recruiter",
        email="recruiter@acmecorp.com",
        phone="+91 9998887776",
        role=Role.COMPANY,
        is_verified=True,
        is_active=True
    )
    user.set_password("CompanyPass@123")
    db.session.add(user)
    db.session.commit()

    profile = CompanyProfile(
        user_id=user.id,
        company_name="Acme Corporation",
        website="https://acmecorp.com",
        industry="Information Technology",
        location="Bengaluru, India",
        description="Pioneering modern enterprise intelligence."
    )
    db.session.add(profile)
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def admin_user(app):
    user = User(
        name="System Administrator",
        email="admin@teleportal.com",
        phone="+91 9000000000",
        role=Role.ADMIN,
        is_verified=True,
        is_active=True
    )
    user.set_password("AdminPass@123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope="function")
def sample_internship(app, company_user):
    cat = Category(name="Artificial Intelligence", slug="artificial-intelligence", icon="bi-cpu")
    db.session.add(cat)
    db.session.commit()

    internship = Internship(
        company_id=company_user.id,
        category_id=cat.id,
        title="Full Stack AI Intern",
        slug="full-stack-ai-intern-1",
        description="Exciting internship working on cutting edge AI applications with Flask and PyTorch.",
        requirements="Python, REST APIs, Git, Machine Learning basics",
        skills="Python, Flask, Docker, Machine Learning",
        location="Remote",
        internship_type="Virtual",
        stipend_type="Fixed",
        duration_weeks=12,
        stipend_amount=25000,
        openings=3,
        deadline=date.today() + timedelta(days=30),
        is_active=True
    )
    db.session.add(internship)
    db.session.commit()
    return internship