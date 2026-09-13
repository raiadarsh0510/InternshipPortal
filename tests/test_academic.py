from app.services.academic_service import academic_service
from app.models.academic import AcademicEvaluation
from app.models.application import Application, ApplicationStatus

def test_nep_evaluation_grade_outstanding(app, student_user, company_user, sample_internship):
    from app.extensions import db
    app_record = Application(
        student_id=student_user.id,
        internship_id=sample_internship.id,
        status=ApplicationStatus.ACCEPTED
    )
    db.session.add(app_record)
    db.session.commit()

    evaluation = academic_service.submit_evaluation(
        application_id=app_record.id,
        student_id=student_user.id,
        company_id=company_user.id,
        college_name="IIT Delhi",
        faculty_mentor_name="Dr. V. Sharma",
        faculty_mentor_email="mentor@iitd.ac.in",
        attendance=98.5,
        tech_comp=5, # out of 5
        professionalism=5,
        proj_comp=5,
        remarks="Exemplary contributions to core production pipelines."
    )

    assert evaluation.nep_credits_awarded == 4
    assert evaluation.grade == "O"
    assert evaluation.overall_performance == 10.0
    assert evaluation.is_verified_by_college is True

def test_nep_evaluation_grade_a(app, student_user, company_user, sample_internship):
    from app.extensions import db
    app_record = Application(
        student_id=student_user.id,
        internship_id=sample_internship.id,
        status=ApplicationStatus.ACCEPTED
    )
    db.session.add(app_record)
    db.session.commit()

    evaluation = academic_service.submit_evaluation(
        application_id=app_record.id,
        student_id=student_user.id,
        company_id=company_user.id,
        college_name="NIT Trichy",
        faculty_mentor_name="Prof. Rao",
        faculty_mentor_email="rao@nitt.edu",
        attendance=90.0,
        tech_comp=4,
        professionalism=4,
        proj_comp=4,
        remarks="Consistent and reliable team contributor."
    )

    assert evaluation.nep_credits_awarded == 4
    assert evaluation.grade == "A+"
    assert evaluation.overall_performance == 8.0

def test_student_nep_evaluations_page(client, student_user, company_user, sample_internship):
    from app.extensions import db
    app_record = Application(
        student_id=student_user.id,
        internship_id=sample_internship.id,
        status=ApplicationStatus.ACCEPTED
    )
    db.session.add(app_record)
    db.session.commit()

    academic_service.submit_evaluation(
        application_id=app_record.id,
        student_id=student_user.id,
        company_id=company_user.id,
        college_name="IIT Delhi",
        faculty_mentor_name="Dr. Sharma",
        faculty_mentor_email="mentor@iitd.ac.in",
        attendance=95.0,
        tech_comp=5,
        professionalism=5,
        proj_comp=5,
        remarks="Excellent performance"
    )

    client.post("/login", data={
        "email": student_user.email,
        "password": "StudentPass@123"
    })

    res = client.get("/student/nep-evaluations")
    assert res.status_code == 200
    assert b"NEP 2020" in res.data
    assert b"IIT Delhi" in res.data