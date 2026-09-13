from datetime import datetime
import json
from app.extensions import db

class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    overall_score = db.Column(db.Integer, default=0) # 0-100
    ats_score = db.Column(db.Integer, default=0)
    readability_score = db.Column(db.Integer, default=0)
    skills_detected = db.Column(db.Text) # JSON string
    missing_critical_skills = db.Column(db.Text) # JSON string
    suggestions = db.Column(db.Text) # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="resume_analyses")

    def get_skills(self):
        return json.loads(self.skills_detected) if self.skills_detected else []

    def get_missing(self):
        return json.loads(self.missing_critical_skills) if self.missing_critical_skills else []

    def get_suggestions(self):
        return json.loads(self.suggestions) if self.suggestions else []

class MockInterviewSession(db.Model):
    __tablename__ = "mock_interview_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_role = db.Column(db.String(120), nullable=False)
    interview_type = db.Column(db.String(30), default="Technical")
    questions_json = db.Column(db.Text) # JSON list
    answers_json = db.Column(db.Text) # JSON list
    evaluations_json = db.Column(db.Text) # JSON list
    overall_score = db.Column(db.Integer, default=0) # 0-100
    final_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="mock_interviews")

class SkillGapReport(db.Model):
    __tablename__ = "skill_gap_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_role = db.Column(db.String(120), nullable=False)
    current_skills = db.Column(db.Text) # JSON
    required_skills = db.Column(db.Text) # JSON
    missing_skills = db.Column(db.Text) # JSON
    learning_roadmap = db.Column(db.Text) # JSON or Markdown
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="skill_gap_reports")

class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender = db.Column(db.String(20), nullable=False) # user or ai
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="chats")