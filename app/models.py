from datetime import datetime

from flask_login import UserMixin
from app.database import db


# ==========================================
# User Model
# ==========================================
class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    phone = db.Column(db.String(15))

    college = db.Column(db.String(150))

    branch = db.Column(db.String(100))

    year = db.Column(db.String(20))

    skills = db.Column(db.String(500))

    bio = db.Column(db.Text)

    resume = db.Column(db.String(255))

    profile_image = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    internships = db.relationship(
        "Internship",
        backref="owner",
        lazy=True,
        foreign_keys="Internship.posted_by"
    )

    applications = db.relationship(
        "Application",
        backref="student",
        lazy=True
    )

    saved = db.relationship(
        "SavedInternship",
        backref="student_user",
        lazy=True
    )

    def __repr__(self):

        return f"<User {self.name}>"


# ==========================================
# Internship Model
# ==========================================
class Internship(db.Model):

    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    company = db.Column(db.String(200), nullable=False)

    company_logo = db.Column(db.String(200))

    category = db.Column(db.String(100))

    internship_type = db.Column(db.String(50))

    experience = db.Column(db.String(50))

    responsibilities = db.Column(db.Text)

    requirements = db.Column(db.Text)

    benefits = db.Column(db.Text)

    location = db.Column(db.String(100), nullable=False)

    stipend = db.Column(db.Integer)

    duration = db.Column(db.String(50))

    skills = db.Column(db.String(300))

    description = db.Column(db.Text)

    last_date = db.Column(db.Date, nullable=False)

    posted_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    applications = db.relationship(
        "Application",
        backref="internship",
        cascade="all, delete",
        lazy=True
    )

    saved = db.relationship(
        "SavedInternship",
        backref="saved_internship",
        cascade="all, delete",
        lazy=True
    )

    def __repr__(self):

        return f"<Internship {self.title}>"


# ==========================================
# Application Model
# ==========================================
class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"<Application {self.id}>"


# ==========================================
# Saved Internship Model
# ==========================================
class SavedInternship(db.Model):

    __tablename__ = "saved_internships"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    internship_id = db.Column(
        db.Integer,
        db.ForeignKey("internships.id"),
        nullable=False
    )

    saved_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"<SavedInternship {self.id}>"