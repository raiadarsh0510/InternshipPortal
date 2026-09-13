from datetime import datetime
from app.extensions import db

class AcademicEvaluation(db.Model):
    __tablename__ = "academic_evaluations"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), unique=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    college_name = db.Column(db.String(180))
    faculty_mentor_name = db.Column(db.String(120))
    faculty_mentor_email = db.Column(db.String(120))
    
    attendance_percentage = db.Column(db.Float, default=100.0)
    technical_competence = db.Column(db.Integer, default=5) # 1-5
    professionalism = db.Column(db.Integer, default=5) # 1-5
    project_completion = db.Column(db.Integer, default=5) # 1-5
    overall_performance = db.Column(db.Float, default=10.0) # 1-10
    
    nep_credits_awarded = db.Column(db.Integer, default=4) # 2-6 credits under NEP 2020 guidelines
    grade = db.Column(db.String(5), default="A+") # O, A+, A, B+, B
    company_remarks = db.Column(db.Text)
    faculty_remarks = db.Column(db.Text)
    
    is_verified_by_college = db.Column(db.Boolean, default=False)
    verified_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", foreign_keys=[student_id])
    company = db.relationship("User", foreign_keys=[company_id])