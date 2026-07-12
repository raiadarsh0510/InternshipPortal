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
        "mysql+pymysql://root:1234@localhost/internship_portal"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

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