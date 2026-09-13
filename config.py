import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    # ==========================================
    # Security
    # ==========================================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "internship_portal_secret_key"
    )

    # ==========================================
    # Database
    # ==========================================
    _raw_db_url = os.getenv("DATABASE_URL")
    if _raw_db_url:
        # Normalize MySQL driver for PyMySQL
        if _raw_db_url.startswith("mysql://"):
            _raw_db_url = _raw_db_url.replace("mysql://", "mysql+pymysql://", 1)
        # Normalize Postgres scheme for modern SQLAlchemy
        elif _raw_db_url.startswith("postgres://"):
            _raw_db_url = _raw_db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _raw_db_url
    else:
        # Fallback to local SQLite instance db
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'internship_portal.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==========================================
    # Email / Verification
    # ==========================================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        "no-reply@internshipportal.local"
    )

    # ==========================================
    # AI / Generative Models
    # ==========================================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # ==========================================
    # Upload Folders
    # ==========================================
    PROFILE_UPLOAD_FOLDER = os.path.join(basedir, "static", "images", "profiles")

    COMPANY_LOGO_FOLDER = os.path.join(basedir, "static", "images", "company_logos")

    RESUME_UPLOAD_FOLDER = os.path.join(basedir, "static", "resumes")

    # ==========================================
    # Upload Restrictions
    # ==========================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    ALLOWED_RESUME_EXTENSIONS = {
        "pdf",
        "doc",
        "docx"
    }
