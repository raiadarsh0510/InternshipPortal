import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

def get_database_uri():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("mysql://"):
            return db_url.replace("mysql://", "mysql+pymysql://", 1)
        if db_url.startswith("postgres://"):
            return db_url.replace("postgres://", "postgresql://", 1)
        return db_url
    instance_path = os.path.join(basedir, "instance")
    os.makedirs(instance_path, exist_ok=True)
    return f"sqlite:///{os.path.join(instance_path, 'teleportal.db')}"

class Config:
    PROJECT_NAME = "TELEPORTAL"
    PROJECT_TAGLINE = "A Next Generation AI Powered Internship Management Platform"
    VERSION = "2.0.0"

    SECRET_KEY = os.getenv("SECRET_KEY", "teleportal-enterprise-secret-key-2026-srdt")
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Security & Sessions
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 7200

    # Rate Limiter
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "memory://")

    # Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@teleportal.ai")

    # AI Service Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Uploads
    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    PROFILE_UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads", "profiles")
    COMPANY_LOGO_FOLDER = os.path.join(basedir, "app", "static", "uploads", "company_logos")
    RESUME_UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads", "resumes")
    CERTIFICATE_UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads", "certificates")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "svg"}
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

config_by_name = {
    "dev": DevelopmentConfig,
    "development": DevelopmentConfig,
    "prod": ProductionConfig,
    "production": ProductionConfig,
    "test": TestingConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}