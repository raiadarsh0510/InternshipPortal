from flask import render_template
from flask_login import login_required, current_user

from app.models import Internship, Application


def init_dashboard_routes(app):

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():

        if current_user.role.lower() == "company":

            internships = Internship.query.filter_by(
                posted_by=current_user.id
            ).all()

            internship_ids = [i.id for i in internships]

            total_posted = len(internships)

            total_applications = Application.query.filter(
                Application.internship_id.in_(internship_ids)
            ).count() if internship_ids else 0

            accepted = Application.query.filter(
                Application.internship_id.in_(internship_ids),
                Application.status == "Accepted"
            ).count() if internship_ids else 0

            rejected = Application.query.filter(
                Application.internship_id.in_(internship_ids),
                Application.status == "Rejected"
            ).count() if internship_ids else 0

            pending = Application.query.filter(
                Application.internship_id.in_(internship_ids),
                Application.status == "Pending"
            ).count() if internship_ids else 0

            return render_template(
                "dashboard.html",
                total_posted=total_posted,
                total_applications=total_applications,
                accepted=accepted,
                rejected=rejected,
                pending=pending
            )

        total_applications = Application.query.filter_by(
            student_id=current_user.id
        ).count()

        accepted = Application.query.filter_by(
            student_id=current_user.id,
            status="Accepted"
        ).count()

        rejected = Application.query.filter_by(
            student_id=current_user.id,
            status="Rejected"
        ).count()

        pending = Application.query.filter_by(
            student_id=current_user.id,
            status="Pending"
        ).count()

        return render_template(
            "dashboard.html",
            total_applications=total_applications,
            accepted=accepted,
            rejected=rejected,
            pending=pending
        )
    
    