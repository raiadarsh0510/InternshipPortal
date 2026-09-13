from app.routes.auth_bp import auth_bp
from app.routes.student_bp import student_bp
from app.routes.company_bp import company_bp
from app.routes.admin_bp import admin_bp
from app.routes.internship_bp import internship_bp
from app.routes.ai_bp import ai_bp
from app.routes.api_bp import api_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(internship_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(api_bp)