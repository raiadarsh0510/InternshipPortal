from datetime import datetime
from app.extensions import db

class ApplicationStatus:
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

    ALL = [APPLIED, UNDER_REVIEW, SHORTLISTED, INTERVIEW_SCHEDULED, ACCEPTED, REJECTED, WITHDRAWN]

class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=False, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    resume_path = db.Column(db.String(255))
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(30), default=ApplicationStatus.APPLIED, nullable=False, index=True)
    match_score = db.Column(db.Integer, default=0) # 0-100 computed AI compatibility
    employer_notes = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    status_history = db.relationship("ApplicationStatusHistory", backref="application", lazy="dynamic", cascade="all, delete-orphan")
    interviews = db.relationship("InterviewSchedule", backref="application", lazy="dynamic", cascade="all, delete-orphan")
    academic_evaluation = db.relationship("AcademicEvaluation", backref="application", uselist=False, cascade="all, delete-orphan")

class ApplicationStatusHistory(db.Model):
    __tablename__ = "application_status_history"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    old_status = db.Column(db.String(30))
    new_status = db.Column(db.String(30), nullable=False)
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SavedInternship(db.Model):
    __tablename__ = "saved_internships"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"), nullable=False, index=True)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", backref="saved_internships")