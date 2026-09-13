import pytest
from app.models.user import User, Role

def test_login_page_renders(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign In" in response.data or b"Login" in response.data

def test_login_successful_student(client, student_user):
    response = client.post("/login", data={
        "email": "student@test.com",
        "password": "StudentPass@123"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "/student/dashboard" in response.headers["Location"]

def test_login_successful_company(client, company_user):
    response = client.post("/login", data={
        "email": "recruiter@acmecorp.com",
        "password": "CompanyPass@123"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "/company/dashboard" in response.headers["Location"]

def test_login_invalid_password(client, student_user):
    response = client.post("/login", data={
        "email": "student@test.com",
        "password": "WrongPassword123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data

def test_student_registration(client):
    response = client.post("/register?role=student", data={
        "name": "New Candidate",
        "email": "candidate@university.edu",
        "password": "SecurePassword123",
        "confirm_password": "SecurePassword123",
        "phone": "9876543210",
        "college": "National Institute of Technology",
        "branch": "Computer Science"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "/student/dashboard" in response.headers["Location"]
    
    # Verify user saved in database
    user = User.query.filter_by(email="candidate@university.edu").first()
    assert user is not None
    assert user.role == Role.STUDENT
    assert user.student_profile is not None
    assert user.student_profile.college == "National Institute of Technology"

def test_company_registration(client):
    response = client.post("/register?role=company", data={
        "company_name": "NextGen Systems",
        "hr_name": "Elena Rostova",
        "email": "elena@nextgensystems.io",
        "password": "CompanySecretPass123",
        "confirm_password": "CompanySecretPass123",
        "location": "Hyderabad, India",
        "website": "https://nextgensystems.io"
    }, follow_redirects=False)
    assert response.status_code == 302
    assert "/company/dashboard" in response.headers["Location"]

    user = User.query.filter_by(email="elena@nextgensystems.io").first()
    assert user is not None
    assert user.role == Role.COMPANY
    assert user.company_profile is not None
    assert user.company_profile.company_name == "NextGen Systems"

def test_protected_routes_redirect_anonymous(client):
    r1 = client.get("/student/dashboard")
    assert r1.status_code == 302
    assert "/login" in r1.headers["Location"]

    r2 = client.get("/company/dashboard")
    assert r2.status_code == 302
    assert "/login" in r2.headers["Location"]

    r3 = client.get("/admin/dashboard")
    assert r3.status_code == 302
    assert "/login" in r3.headers["Location"]

def test_logout(client, student_user):
    # Log in first
    client.post("/login", data={
        "email": "student@test.com",
        "password": "StudentPass@123"
    })
    # Now log out
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]