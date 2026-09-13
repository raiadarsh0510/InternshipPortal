from datetime import datetime
from app.extensions import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(90), unique=True, nullable=False)
    icon = db.Column(db.String(50), default="briefcase")
    internships = db.relationship("Internship", backref="category_rel", lazy="dynamic")

class Internship(db.Model):
    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    
    internship_type = db.Column(db.String(50), default="Full-time") # Full-time, Part-time, Virtual, Hybrid, On-site
    experience_level = db.Column(db.String(50), default="Fresher") # Fresher, Intermediate, Advanced
    location = db.Column(db.String(120), nullable=False)
    
    stipend_type = db.Column(db.String(30), default="Fixed") # Fixed, Performance, Unpaid
    stipend_amount = db.Column(db.Integer, default=0)
    duration_weeks = db.Column(db.Integer, default=8)
    openings = db.Column(db.Integer, default=1)
    
    description = db.Column(db.Text, nullable=False)
    responsibilities = db.Column(db.Text)
    requirements = db.Column(db.Text)
    skills = db.Column(db.String(400)) # Comma separated
    benefits = db.Column(db.Text)
    
    deadline = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_featured = db.Column(db.Boolean, default=False)
    has_ppo_opportunity = db.Column(db.Boolean, default=False)
    
    views_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship("Application", backref="internship_rel", lazy="dynamic", cascade="all, delete-orphan")
    saved_by = db.relationship("SavedInternship", backref="internship_ref", lazy="dynamic", cascade="all, delete-orphan")

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def __repr__(self):
        return f"<Internship {self.title}>"

class MicroProject(db.Model):
    __tablename__ = "micro_projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    bounty_amount = db.Column(db.Integer, default=0)
    estimated_hours = db.Column(db.Integer, default=15)
    skills_required = db.Column(db.String(300))
    deliverable_description = db.Column(db.Text, nullable=False)
    submission_deadline = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("User", backref="bounties_posted")
    submissions = db.relationship("MicroSubmission", backref="project", lazy="dynamic", cascade="all, delete-orphan")

class MicroSubmission(db.Model):
    __tablename__ = "micro_submissions"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("micro_projects.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    submission_url = db.Column(db.String(255), nullable=False)
    github_pr_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    status = db.Column(db.String(30), default="submitted") # submitted, under_review, approved, rejected
    reviewer_feedback = db.Column(db.Text)
    score = db.Column(db.Integer) # 1-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", backref="micro_submissions")