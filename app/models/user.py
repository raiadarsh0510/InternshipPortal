from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class Role:
    STUDENT = "student"
    COMPANY = "company"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

    ALL = [STUDENT, COMPANY, ADMIN, SUPER_ADMIN]

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default=Role.STUDENT, nullable=False, index=True)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)

    # Relationships
    student_profile = db.relationship("UserProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship("CompanyProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    posted_internships = db.relationship("Internship", backref="company_user", lazy="dynamic", foreign_keys="Internship.company_id")
    applications = db.relationship("Application", backref="applicant", lazy="dynamic", foreign_keys="Application.student_id")
    notifications = db.relationship("Notification", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    audit_logs = db.relationship("AuditLog", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_student(self):
        return self.role == Role.STUDENT

    @property
    def is_company(self):
        return self.role == Role.COMPANY

    @property
    def is_admin(self):
        return self.role in [Role.ADMIN, Role.SUPER_ADMIN]

    @property
    def is_super_admin(self):
        return self.role == Role.SUPER_ADMIN

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"

class UserProfile(db.Model):
    __tablename__ = "user_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    college = db.Column(db.String(180))
    branch = db.Column(db.String(100))
    graduation_year = db.Column(db.String(10))
    cgpa = db.Column(db.Float)
    skills = db.Column(db.Text)  # Comma-separated or tags
    bio = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    profile_image = db.Column(db.String(255), default="default_profile.png")
    
    # Portfolio Links
    github_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    leetcode_url = db.Column(db.String(255))
    codeforces_url = db.Column(db.String(255))
    portfolio_url = db.Column(db.String(255))
    
    achievements = db.Column(db.Text)
    certifications = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(160), unique=True, index=True)
    logo_path = db.Column(db.String(255), default="default_company.png")
    banner_path = db.Column(db.String(255))
    website = db.Column(db.String(255))
    location = db.Column(db.String(150))
    industry = db.Column(db.String(100))
    company_size = db.Column(db.String(50))
    description = db.Column(db.Text)
    cin_number = db.Column(db.String(50))
    is_cin_verified = db.Column(db.Boolean, default=False)
    hr_contact_name = db.Column(db.String(100))
    hr_contact_email = db.Column(db.String(120))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OTPVerification(db.Model):
    __tablename__ = "otp_verifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    otp_code = db.Column(db.String(10), nullable=False)
    purpose = db.Column(db.String(30), nullable=False) # email_verify, password_reset, 2fa
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)