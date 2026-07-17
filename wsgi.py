from flask import Flask
from flask_login import LoginManager

from config import Config
from app.database import db

# Models
from app.models import (
    User,
    Internship,
    Application,
    SavedInternship,
    ChatMessage
)

# Register Routes
from app.routes import init_routes


# ==========================================
# Create Flask App
# ==========================================
app = Flask(__name__)

# ==========================================
# Configuration
# ==========================================
app.config.from_object(Config)

# Secret Key
app.secret_key = app.config.get(
    "SECRET_KEY",
    "internship_portal_secret_key"
)

# ==========================================
# Initialize Extensions
# ==========================================
db.init_app(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Please login to continue."
)

login_manager.login_message_category = "warning"

login_manager.session_protection = "strong"


# ==========================================
# User Loader
# ==========================================
@login_manager.user_loader
def load_user(user_id):

    return db.session.get(
        User,
        int(user_id)
    )


# ==========================================
# Create Database Tables
# ==========================================
with app.app_context():

    db.create_all()


# ==========================================
# Register Application Routes
# ==========================================
init_routes(app)


# ==========================================
# Show Registered Routes
# ==========================================
if app.debug:

    print("\n========== REGISTERED ROUTES ==========\n")

    for rule in sorted(
        app.url_map.iter_rules(),
        key=lambda r: r.rule
    ):

        print(
            f"{rule.endpoint:<30} {rule.rule}"
        )

    print("\n=======================================\n")


# ==========================================
# Run Application
# ==========================================
if __name__ == "__main__":

    app.run(
        debug=True
    )