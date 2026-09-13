from app.repositories.base import BaseRepository
from app.models.application import Application, SavedInternship
from app.extensions import db

class ApplicationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Application)

    def get_by_student(self, student_id):
        return Application.query.filter_by(student_id=student_id).order_by(Application.applied_at.desc()).all()

    def get_by_internship(self, internship_id):
        return Application.query.filter_by(internship_id=internship_id).order_by(Application.applied_at.desc()).all()

    def has_applied(self, student_id, internship_id):
        return Application.query.filter_by(student_id=student_id, internship_id=internship_id).first() is not None

    def is_saved(self, student_id, internship_id):
        return SavedInternship.query.filter_by(student_id=student_id, internship_id=internship_id).first() is not None