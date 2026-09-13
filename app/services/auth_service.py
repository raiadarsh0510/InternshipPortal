import random
from datetime import datetime, timedelta
from flask import current_app
from app.extensions import db
from app.models.user import User, UserProfile, CompanyProfile, Role
from app.repositories import user_repo

class AuthService:
    @staticmethod
    def register_student(name, email, password, phone=None, college=None, branch=None):
        existing = user_repo.get_by_email(email)
        if existing:
            return None, "Email address is already registered."
        
        user = User(
            name=name.strip(),
            email=email.strip().lower(),
            role=Role.STUDENT,
            phone=phone.strip() if phone else None,
            is_verified=True # Auto-verified for seamless UX, OTP can be optionally triggered
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = UserProfile(
            user_id=user.id,
            college=college,
            branch=branch
        )
        db.session.add(profile)
        db.session.commit()
        return user, None

    @staticmethod
    def register_company(company_name, hr_name, email, password, location=None, website=None):
        existing = user_repo.get_by_email(email)
        if existing:
            return None, "Email address is already registered."

        user = User(
            name=hr_name.strip(),
            email=email.strip().lower(),
            role=Role.COMPANY,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        import re
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", company_name.strip().lower()).strip("-")[:150]
        
        company_profile = CompanyProfile(
            user_id=user.id,
            company_name=company_name.strip(),
            slug=slug,
            location=location,
            website=website,
            hr_contact_name=hr_name,
            hr_contact_email=email
        )
        db.session.add(company_profile)
        db.session.commit()
        return user, None

    @staticmethod
    def authenticate(email, password):
        user = user_repo.get_by_email(email)
        if user and user.is_active and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None

    @staticmethod
    def generate_otp(user_id, purpose="email_verify"):
        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        user_repo.create_otp(user_id, otp_code, purpose, expires_at)
        return otp_code

    @staticmethod
    def verify_otp(user_id, otp_code, purpose="email_verify"):
        return user_repo.verify_otp(user_id, otp_code, purpose)

auth_service = AuthService()