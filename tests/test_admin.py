from app.models.user import User, Role
from app.models.internship import Internship
from app.models.system import Announcement, AuditLog

def test_admin_dashboard_stats(client, admin_user):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })
    res = client.get("/admin/dashboard")
    assert res.status_code == 200
    assert b"Platform Control Center" in res.data
    assert b"SYSTEM ADMINISTRATION" in res.data

def test_admin_manage_users(client, admin_user, student_user, company_user):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })
    res = client.get("/admin/users")
    assert res.status_code == 200
    assert b"User Governance Directory" in res.data
    assert b"Test Student" in res.data
    assert b"Test Recruiter" in res.data

def test_admin_toggle_user_status(client, admin_user, student_user):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })
    
    assert student_user.is_active is True

    # Suspend user
    res = client.post(f"/admin/user/{student_user.id}/toggle-status", follow_redirects=False)
    assert res.status_code == 302
    
    from app.extensions import db
    db.session.refresh(student_user)
    assert student_user.is_active is False

def test_admin_moderate_internship(client, admin_user, sample_internship):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })

    assert sample_internship.is_active is True

    res = client.post(f"/admin/internship/{sample_internship.id}/toggle", follow_redirects=False)
    assert res.status_code == 302

    from app.extensions import db
    db.session.refresh(sample_internship)
    assert sample_internship.is_active is False

def test_admin_broadcast_announcement(client, admin_user):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })

    res = client.post("/admin/announcements", data={
        "title": "NEP 2020 Compliance Deadline Notice",
        "content": "All affiliated universities must verify credits by the end of this month.",
        "target_role": "all"
    }, follow_redirects=False)

    assert res.status_code == 302

    ann = Announcement.query.filter_by(title="NEP 2020 Compliance Deadline Notice").first()
    assert ann is not None
    assert ann.target_role == "all"

def test_admin_audit_logs_view(client, admin_user):
    client.post("/login", data={
        "email": admin_user.email,
        "password": "AdminPass@123"
    })
    res = client.get("/admin/audit-logs")
    assert res.status_code == 200
    assert b"Security & Compliance Audit Trail" in res.data

def test_student_forbidden_admin_access(client, student_user):
    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })
    res = client.get("/admin/dashboard", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]