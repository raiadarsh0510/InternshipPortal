import os


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
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///internship_portal.db"
    )

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
    PROFILE_UPLOAD_FOLDER = "static/images/profiles"

    COMPANY_LOGO_FOLDER = "static/images/company_logos"

    RESUME_UPLOAD_FOLDER = "static/resumes"

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
