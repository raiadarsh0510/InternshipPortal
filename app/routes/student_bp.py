from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.application import Application, SavedInternship
from app.models.internship import Internship
from app.models.academic import AcademicEvaluation
from app.models.interview import InterviewSchedule
from app.forms import StudentProfileForm
from app.services import security_service

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.before_request
@login_required
def check_student():
    if not current_user.is_student and not current_user.is_admin:
        flash("Unauthorized access. Student credentials required.", "danger")
        return redirect(url_for("auth.login"))

@student_bp.route("/dashboard")
def dashboard():
    apps = Application.query.filter_by(student_id=current_user.id).all()
    saved = SavedInternship.query.filter_by(student_id=current_user.id).all()
    interviews = InterviewSchedule.query.filter_by(student_id=current_user.id, status="scheduled").all()
    evals = AcademicEvaluation.query.filter_by(student_id=current_user.id).all()

    stats = {
        "applied": len(apps),
        "shortlisted": len([a for a in apps if a.status == "shortlisted"]),
        "interviews": len(interviews),
        "accepted": len([a for a in apps if a.status == "accepted"]),
        "saved": len(saved),
        "nep_credits": sum([e.nep_credits_awarded for e in evals if e.is_verified_by_college])
    }

    # Recommended internships based on skills
    skills_list = current_user.student_profile.get_skills_list() if current_user.student_profile else []
    recommended = Internship.query.filter_by(is_active=True).order_by(Internship.created_at.desc()).limit(4).all()

    return render_template("student/dashboard.html", stats=stats, recent_apps=apps[:5], upcoming_interviews=interviews, recommended=recommended)

@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    profile_obj = current_user.student_profile
    form = StudentProfileForm(obj=profile_obj)
    
    if request.method == "GET":
        form.name.data = current_user.name

    if form.validate_on_submit():
        current_user.name = form.name.data
        if not profile_obj:
            from app.models.user import UserProfile
            profile_obj = UserProfile(user_id=current_user.id)
            db.session.add(profile_obj)
            
        profile_obj.college = form.college.data
        profile_obj.branch = form.branch.data
        profile_obj.graduation_year = form.graduation_year.data
        profile_obj.cgpa = form.cgpa.data
        profile_obj.skills = form.skills.data
        profile_obj.bio = form.bio.data
        profile_obj.github_url = form.github_url.data
        profile_obj.linkedin_url = form.linkedin_url.data
        profile_obj.leetcode_url = form.leetcode_url.data
        profile_obj.codeforces_url = form.codeforces_url.data
        profile_obj.portfolio_url = form.portfolio_url.data
        
        db.session.commit()
        security_service.log_action(current_user.id, "PROFILE_UPDATE", "user_profile", profile_obj.id, "Updated student profile")
        flash("Your profile and portfolio links have been updated successfully!", "success")
        return redirect(url_for("student.profile"))

    return render_template("student/profile.html", form=form, profile=profile_obj)

@student_bp.route("/applications")
def applications():
    apps = Application.query.filter_by(student_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template("student/applications.html", applications=apps)

@student_bp.route("/saved")
def saved_internships():
    saved = SavedInternship.query.filter_by(student_id=current_user.id).order_by(SavedInternship.saved_at.desc()).all()
    return render_template("student/saved.html", saved_list=saved)

@student_bp.route("/nep-evaluations")
def nep_evaluations():
    evals = AcademicEvaluation.query.filter_by(student_id=current_user.id).order_by(AcademicEvaluation.created_at.desc()).all()
    return render_template("student/nep_evaluations.html", evaluations=evals)