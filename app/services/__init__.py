from app.services.auth_service import auth_service
from app.services.ai_service import ai_service
from app.services.internship_service import internship_service
from app.services.application_service import application_service
from app.services.academic_service import academic_service
from app.services.notification_service import notification_service, security_service

__all__ = [
    "auth_service", "ai_service", "internship_service",
    "application_service", "academic_service", "notification_service", "security_service"
]