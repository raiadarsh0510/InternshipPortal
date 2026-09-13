import os
from flask import Flask, render_template
from config import config_by_name, Config
from app.extensions import db, migrate, login_manager, csrf, mail, limiter
from app.routes import register_blueprints
from app.models.user import User

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "dev")
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_by_name.get(config_name, Config))

    # Ensure required runtime folders exist
    for folder in [
        os.path.join(app.root_path, "..", "instance"),
        app.config.get("UPLOAD_FOLDER"),
        app.config.get("PROFILE_UPLOAD_FOLDER"),
        app.config.get("COMPANY_LOGO_FOLDER"),
        app.config.get("RESUME_UPLOAD_FOLDER"),
        app.config.get("CERTIFICATE_UPLOAD_FOLDER")
    ]:
        if folder:
            os.makedirs(folder, exist_ok=True)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    register_blueprints(app)

    # Context Processors
    @app.context_processor
    def inject_globals():
        return {
            "PROJECT_NAME": app.config.get("PROJECT_NAME", "TELEPORTAL"),
            "PROJECT_TAGLINE": app.config.get("PROJECT_TAGLINE", "AI-Powered Internship Platform"),
            "VERSION": app.config.get("VERSION", "2.0.0")
        }

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(429)
    def ratelimit_exceeded(e):
        return render_template("errors/429.html"), 429

    # Create tables automatically for initial convenience
    with app.app_context():
        db.create_all()

    return app