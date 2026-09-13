from datetime import datetime
from flask import request
from app.extensions import db
from app.models.system import Notification, AuditLog

class NotificationService:
    @staticmethod
    def send_notification(user_id, title, message, link=None):
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            link=link
        )
        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def get_unread(user_id, limit=5):
        return Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).limit(limit).all()

notification_service = NotificationService()

class SecurityService:
    @staticmethod
    def log_action(user_id, action, entity_type=None, entity_id=None, details=None):
        try:
            ip = request.remote_addr if request else "127.0.0.1"
            ua = request.user_agent.string[:250] if request and request.user_agent else "System"
        except Exception:
            ip = "127.0.0.1"
            ua = "Internal"

        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            ip_address=ip,
            user_agent=ua,
            details=details
        )
        db.session.add(log)
        db.session.commit()
        return log

security_service = SecurityService()