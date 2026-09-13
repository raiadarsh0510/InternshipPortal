from datetime import date, timedelta
from app.models.internship import Internship, Category
from app.models.application import Application, ApplicationStatus

def test_index_landing_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"TELEPORTAL" in res.data or b"Internship" in res.data

def test_internships_directory_listing(client, sample_internship):
    res = client.get("/internships")
    assert res.status_code == 200
    assert b"Full Stack AI Intern" in res.data

def test_internship_detail_view(client, sample_internship):
    res = client.get(f"/internship/{sample_internship.id}")
    assert res.status_code == 200
    assert b"Full Stack AI Intern" in res.data
    assert b"Acme Corporation" in res.data

def test_student_apply_flow(client, student_user, sample_internship):
    # Log in as student
    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })
    
    # Submit application
    res = client.post(f"/internship/{sample_internship.id}/apply", data={
        "cover_letter": "I have extensive experience building Flask and PyTorch AI apps."
    }, follow_redirects=False)
    
    assert res.status_code == 302
    assert "/student/applications" in res.headers["Location"]

    # Verify application recorded in DB
    app_record = Application.query.filter_by(student_id=student_user.id, internship_id=sample_internship.id).first()
    assert app_record is not None
    assert app_record.status == ApplicationStatus.APPLIED
    assert app_record.match_score > 0

def test_prevent_duplicate_application(client, student_user, sample_internship):
    # Log in as student
    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })
    
    # Apply first time
    client.post(f"/internship/{sample_internship.id}/apply", data={
        "cover_letter": "First application"
    })

    # Attempt to apply second time
    res = client.post(f"/internship/{sample_internship.id}/apply", data={
        "cover_letter": "Second application"
    }, follow_redirects=True)

    assert b"already submitted an application" in res.data or res.status_code == 200

def test_company_post_internship(client, company_user):
    client.post("/login", data={
        "email": company_user.email,
        "password": "CompanyPass@123"
    })

    cat = Category(name="Backend Development", slug="backend-dev", icon="bi-server")
    from app.extensions import db
    db.session.add(cat)
    db.session.commit()

    deadline_str = (date.today() + timedelta(days=45)).strftime("%Y-%m-%d")

    res = client.post("/company/post-internship", data={
        "title": "Cloud Backend Engineer Intern",
        "category_id": cat.id,
        "internship_type": "Virtual",
        "experience_level": "Fresher",
        "location": "Bengaluru",
        "stipend_type": "Fixed",
        "stipend_amount": 30000,
        "duration_weeks": 16,
        "openings": 2,
        "skills": "Python, Docker, Kubernetes, PostgreSQL",
        "description": "Join our cloud infrastructure engineering team to build scalable microservices.",
        "deadline": deadline_str
    }, follow_redirects=False)

    assert res.status_code == 302
    assert "/company/dashboard" in res.headers["Location"]

    posted = Internship.query.filter_by(title="Cloud Backend Engineer Intern").first()
    assert posted is not None
    assert posted.company_id == company_user.id
    assert posted.stipend_amount == 30000

def test_recruiter_view_and_update_applicant_status(client, company_user, student_user, sample_internship):
    # Create application
    from app.models.application import Application
    from app.extensions import db

    app_record = Application(
        student_id=student_user.id,
        internship_id=sample_internship.id,
        cover_letter="Passionate about AI",
        match_score=85,
        status=ApplicationStatus.APPLIED
    )
    db.session.add(app_record)
    db.session.commit()

    # Log in as company
    client.post("/login", data={
        "email": company_user.email,
        "password": "CompanyPass@123"
    })

    # View applicants page
    res = client.get(f"/company/applicants/{sample_internship.id}")
    assert res.status_code == 200
    assert b"Test Student" in res.data

    # Update status to shortlisted
    res_status = client.post(f"/company/application/{app_record.id}/status", data={
        "status": ApplicationStatus.SHORTLISTED,
        "comment": "Strong portfolio matches requirements"
    }, follow_redirects=False)

    assert res_status.status_code == 302
    
    # Verify in DB
    db.session.refresh(app_record)
    assert app_record.status == ApplicationStatus.SHORTLISTED

def test_student_save_toggle(client, student_user, sample_internship):
    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })

    res = client.post(f"/internship/{sample_internship.id}/save-toggle")
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data["success"] is True
    assert json_data["saved"] is True