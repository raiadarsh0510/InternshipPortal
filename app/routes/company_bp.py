from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.extensions import db
from app.models.internship import Internship, Category
from app.models.application import Application, ApplicationStatus
from app.models.interview import InterviewSchedule
from app.forms import InternshipPostForm
from app.services import internship_service, application_service, academic_service, notification_service, security_service

company_bp = Blueprint("company", __name__, url_prefix="/company")

@company_bp.before_request
@login_required
def check_company():
    if not current_user.is_company and not current_user.is_admin:
        flash("Unauthorized access. Company credentials required.", "danger")
        return redirect(url_for("auth.login"))

@company_bp.route("/dashboard")
def dashboard():
    internships = Internship.query.filter_by(company_id=current_user.id).order_by(Internship.created_at.desc()).all()
    internship_ids = [i.id for i in internships]
    
    total_apps = Application.query.filter(Application.internship_id.in_(internship_ids)).all() if internship_ids else []
    interviews = InterviewSchedule.query.filter_by(company_id=current_user.id).all()

    stats = {
        "active_jobs": len([i for i in internships if i.is_active]),
        "total_applicants": len(total_apps),
        "shortlisted": len([a for a in total_apps if a.status == ApplicationStatus.SHORTLISTED]),
        "interviews_scheduled": len([i for i in interviews if i.status == "scheduled"])
    }

    return render_template("company/dashboard.html", stats=stats, internships=internships[:6], recent_applications=total_apps[:8])

@company_bp.route("/post-internship", methods=["GET", "POST"])
def post_internship():
    form = InternshipPostForm()
    categories = Category.query.all()
    if not categories:
        # Create default categories if none exist
        for cat_name in ["Software Development", "Data Science & AI", "Frontend & UI/UX", "Cybersecurity", "Cloud & DevOps"]:
            c = Category(name=cat_name, slug=cat_name.lower().replace(" ", "-"))
            db.session.add(c)
        db.session.commit()
        categories = Category.query.all()

    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        internship = internship_service.create_internship(
            company_id=current_user.id,
            title=form.title.data,
            category_id=form.category_id.data,
            internship_type=form.internship_type.data,
            location=form.location.data,
            stipend_type=form.stipend_type.data,
            stipend_amount=form.stipend_amount.data,
            duration_weeks=form.duration_weeks.data,
            openings=form.openings.data,
            description=form.description.data,
            responsibilities=form.responsibilities.data,
            requirements=form.requirements.data,
            skills=form.skills.data,
            benefits=form.benefits.data,
            deadline=form.deadline.data
        )
        security_service.log_action(current_user.id, "POST_INTERNSHIP", "internship", internship.id, f"Posted {internship.title}")
        flash("Internship posting published successfully! Verified applicants can now discover it.", "success")
        return redirect(url_for("company.dashboard"))

    return render_template("company/post_internship.html", form=form)

@company_bp.route("/applicants/<int:internship_id>")
def view_applicants(internship_id):
    internship = Internship.query.filter_by(id=internship_id, company_id=current_user.id).first_or_404()
    applicants = Application.query.filter_by(internship_id=internship.id).order_by(Application.match_score.desc()).all()
    return render_template("company/applicants.html", internship=internship, applicants=applicants)

@company_bp.route("/application/<int:application_id>/status", methods=["POST"])
def update_application_status(application_id):
    app = Application.query.get_or_404(application_id)
    if app.internship_rel.company_id != current_user.id and not current_user.is_admin:
        flash("Unauthorized.", "danger")
        return redirect(url_for("company.dashboard"))

    new_status = request.form.get("status")
    comment = request.form.get("comment", "")
    application_service.update_status(app.id, new_status, current_user.id, comment)
    
    # Notify student
    notification_service.send_notification(
        user_id=app.student_id,
        title=f"Application Update: {app.internship_rel.title}",
        message=f"Your application status has been updated to '{new_status.replace('_', ' ').title()}'.",
        link=url_for("student.applications")
    )

    flash(f"Candidate status updated to {new_status.replace('_', ' ').title()}.", "success")
    return redirect(url_for("company.view_applicants", internship_id=app.internship_id))

@company_bp.route("/application/<int:application_id>/schedule-interview", methods=["POST"])
def schedule_interview(application_id):
    app = Application.query.get_or_404(application_id)
    if app.internship_rel.company_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("company.dashboard"))

    date_str = request.form.get("scheduled_at")
    meeting_link = request.form.get("meeting_link", "https://meet.google.com")
    int_type = request.form.get("interview_type", "Technical")
    
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
    except Exception:
        dt = datetime.utcnow()

    interview = InterviewSchedule(
        application_id=app.id,
        company_id=current_user.id,
        student_id=app.student_id,
        interview_type=int_type,
        meeting_link=meeting_link,
        scheduled_at=dt
    )
    db.session.add(interview)
    application_service.update_status(app.id, ApplicationStatus.INTERVIEW_SCHEDULED, current_user.id, f"Scheduled {int_type} interview")
    db.session.commit()

    notification_service.send_notification(
        user_id=app.student_id,
        title="Interview Scheduled!",
        message=f"Your {int_type} interview for {app.internship_rel.title} is scheduled for {dt.strftime('%b %d, %Y %I:%M %p')}.",
        link=url_for("student.dashboard")
    )
    flash("Interview successfully scheduled and candidate notified!", "success")
    return redirect(url_for("company.view_applicants", internship_id=app.internship_id))

@company_bp.route("/application/<int:application_id>/academic-evaluation", methods=["GET", "POST"])
def evaluate_academic(application_id):
    app = Application.query.get_or_404(application_id)
    if app.internship_rel.company_id != current_user.id:
        flash("Unauthorized.", "danger")
        return redirect(url_for("company.dashboard"))

    if request.method == "POST":
        eval_obj = academic_service.submit_evaluation(
            application_id=app.id,
            student_id=app.student_id,
            company_id=current_user.id,
            college_name=request.form.get("college_name", "Autonomous Engineering College"),
            faculty_mentor_name=request.form.get("faculty_mentor_name", "Prof. Academic Mentor"),
            faculty_mentor_email=request.form.get("faculty_mentor_email", "mentor@university.edu"),
            attendance=request.form.get("attendance", 95.0),
            tech_comp=request.form.get("technical_competence", 5),
            professionalism=request.form.get("professionalism", 5),
            proj_comp=request.form.get("project_completion", 5),
            remarks=request.form.get("remarks", "Outstanding project performance.")
        )
        flash(f"Academic evaluation submitted! {eval_obj.nep_credits_awarded} NEP Credits (Grade {eval_obj.grade}) mapped for university.", "success")
        return redirect(url_for("company.view_applicants", internship_id=app.internship_id))

    return render_template("company/evaluate.html", application=app)