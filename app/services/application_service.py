from datetime import datetime
from app.extensions import db
from app.models.application import Application, ApplicationStatus, ApplicationStatusHistory
from app.models.internship import Internship
from app.repositories import application_repo

class ApplicationService:
    @staticmethod
    def apply_to_internship(student_id, internship_id, resume_path, cover_letter, match_score=0):
        if application_repo.has_applied(student_id, internship_id):
            return None, "You have already submitted an application for this internship."
        
        application = Application(
            student_id=student_id,
            internship_id=internship_id,
            resume_path=resume_path,
            cover_letter=cover_letter,
            status=ApplicationStatus.APPLIED,
            match_score=match_score
        )
        db.session.add(application)
        db.session.flush()

        history = ApplicationStatusHistory(
            application_id=application.id,
            old_status=None,
            new_status=ApplicationStatus.APPLIED,
            changed_by_user_id=student_id,
            comment="Application successfully submitted."
        )
        db.session.add(history)
        db.session.commit()
        return application, None

    @staticmethod
    def update_status(application_id, new_status, changed_by_user_id, comment=None):
        app = db.session.get(Application, application_id)
        if not app:
            return None, "Application not found"
        
        old_status = app.status
        app.status = new_status
        history = ApplicationStatusHistory(
            application_id=app.id,
            old_status=old_status,
            new_status=new_status,
            changed_by_user_id=changed_by_user_id,
            comment=comment or f"Status transitioned to {new_status}"
        )
        db.session.add(history)
        db.session.commit()
        return app, None

application_service = ApplicationService()