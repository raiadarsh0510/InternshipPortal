from .auth import init_auth_routes
from .dashboard import init_dashboard_routes
from .profile import init_profile_routes
from .internship import init_internship_routes


def init_routes(app):
    init_auth_routes(app)
    init_dashboard_routes(app)
    init_profile_routes(app)
    init_internship_routes(app)