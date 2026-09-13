from app.repositories.base import BaseRepository
from app.models.user import User, UserProfile, CompanyProfile, OTPVerification
from app.extensions import db

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        if not email:
            return None
        return User.query.filter_by(email=email.strip().lower()).first()

    def get_students_count(self):
        return User.query.filter_by(role="student").count()

    def get_companies_count(self):
        return User.query.filter_by(role="company").count()

    def create_otp(self, user_id, otp_code, purpose, expires_at):
        otp = OTPVerification(user_id=user_id, otp_code=otp_code, purpose=purpose, expires_at=expires_at)
        db.session.add(otp)
        db.session.commit()
        return otp

    def verify_otp(self, user_id, otp_code, purpose):
        from datetime import datetime
        otp = OTPVerification.query.filter(
            OTPVerification.user_id == user_id,
            OTPVerification.otp_code == otp_code,
            OTPVerification.purpose == purpose,
            OTPVerification.is_used == False,
            OTPVerification.expires_at > datetime.utcnow()
        ).first()
        if otp:
            otp.is_used = True
            db.session.commit()
            return True
        return False