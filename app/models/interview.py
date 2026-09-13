from datetime import datetime
from app.extensions import db

class InterviewSchedule(db.Model):
    __tablename__ = "interview_schedules"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    interview_type = db.Column(db.String(40), default="Technical") # Technical, HR, Assessment, Final
    meeting_link = db.Column(db.String(255), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=45)
    status = db.Column(db.String(30), default="scheduled") # scheduled, completed, cancelled, rescheduled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    feedbacks = db.relationship("InterviewFeedback", backref="interview", lazy="dynamic", cascade="all, delete-orphan")
    company = db.relationship("User", foreign_keys=[company_id])
    student = db.relationship("User", foreign_keys=[student_id])

class InterviewFeedback(db.Model):
    __tablename__ = "interview_feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interview_schedules.id"), nullable=False)
    technical_score = db.Column(db.Integer) # 1-10
    communication_score = db.Column(db.Integer) # 1-10
    problem_solving_score = db.Column(db.Integer) # 1-10
    overall_score = db.Column(db.Integer) # 1-10
    comments = db.Column(db.Text)
    recommendation = db.Column(db.String(30)) # hire, hold, reject
    created_at = db.Column(db.DateTime, default=datetime.utcnow)