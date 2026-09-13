from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from app.extensions import db
from app.models.internship import Internship, Category, MicroProject, MicroSubmission
from app.models.application import Application, SavedInternship
from app.repositories import internship_repo, application_repo
from app.services import internship_service, application_service, notification_service

internship_bp = Blueprint("internship", __name__)

@internship_bp.route("/")
def index():
    featured = Internship.query.filter_by(is_active=True).order_by(Internship.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    bounties = MicroProject.query.filter_by(is_active=True).limit(3).all()
    
    total_internships = Internship.query.count()
    total_bounties = MicroProject.query.count()

    stats = {
        "internships": total_internships,
        "companies": 50 + (total_internships * 2),
        "bounties": total_bounties,
        "satisfaction": "98%"
    }
    return render_template("internship/index.html", featured=featured, categories=categories, bounties=bounties, stats=stats)

@internship_bp.route("/internships")
def list_internships():
    keyword = request.args.get("q", "")
    category_id = request.args.get("category", type=int)
    location = request.args.get("location", "")
    work_mode = request.args.get("type", "")
    min_stipend = request.args.get("min_stipend", type=int)
    remote = request.args.get("remote") == "true"
    page = request.args.get("page", 1, type=int)

    query = internship_repo.search_internships(
        keyword=keyword,
        category_id=category_id,
        location=location,
        internship_type=work_mode,
        min_stipend=min_stipend,
        remote_only=remote
    )
    pagination = query.paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.all()

    return render_template(
        "internship/list.html",
        internships=pagination.items,
        pagination=pagination,
        categories=categories,
        filters={
            "q": keyword, "category": category_id, "location": location,
            "type": work_mode, "min_stipend": min_stipend, "remote": remote
        }
    )

@internship_bp.route("/internship/<int:id>")
def detail(id):
    internship = Internship.query.get_or_404(id)
    internship.views_count = (internship.views_count or 0) + 1
    db.session.commit()

    has_applied = False
    is_saved = False
    match_score = 0

    if current_user.is_authenticated and current_user.is_student:
        has_applied = application_repo.has_applied(current_user.id, internship.id)
        is_saved = application_repo.is_saved(current_user.id, internship.id)
        skills = current_user.student_profile.get_skills_list() if current_user.student_profile else []
        match_score = internship_service.calculate_match_score(skills, internship.skills)

    similar = Internship.query.filter(
        Internship.id != internship.id,
        Internship.is_active == True,
        Internship.category_id == internship.category_id
    ).limit(3).all()

    return render_template(
        "internship/detail.html",
        internship=internship,
        has_applied=has_applied,
        is_saved=is_saved,
        match_score=match_score,
        similar=similar
    )

@internship_bp.route("/internship/<int:id>/apply", methods=["POST"])
@login_required
def apply(id):
    if not current_user.is_student:
        flash("Only registered student accounts can apply for internships.", "warning")
        return redirect(url_for("internship.detail", id=id))

    internship = Internship.query.get_or_404(id)
    cover_letter = request.form.get("cover_letter", "")
    resume_path = request.form.get("resume_path") or (current_user.student_profile.resume_path if current_user.student_profile else None)

    skills = current_user.student_profile.get_skills_list() if current_user.student_profile else []
    match_score = internship_service.calculate_match_score(skills, internship.skills)

    app, err = application_service.apply_to_internship(
        student_id=current_user.id,
        internship_id=internship.id,
        resume_path=resume_path,
        cover_letter=cover_letter,
        match_score=match_score
    )

    if err:
        flash(err, "warning")
    else:
        notification_service.send_notification(
            user_id=internship.company_id,
            title="New Internship Applicant!",
            message=f"{current_user.name} applied for {internship.title} with a {match_score}% skill match score.",
            link=url_for("company.view_applicants", internship_id=internship.id)
        )
        flash("Application successfully submitted! The employer has been notified.", "success")

    return redirect(url_for("student.applications"))

@internship_bp.route("/internship/<int:id>/save-toggle", methods=["POST"])
@login_required
def toggle_save(id):
    if not current_user.is_student:
        return jsonify({"success": False, "message": "Students only"}), 403
    saved = internship_service.toggle_save_internship(current_user.id, id)
    return jsonify({"success": True, "saved": saved})

@internship_bp.route("/micro-bounties")
def micro_bounties():
    bounties = MicroProject.query.filter_by(is_active=True).order_by(MicroProject.created_at.desc()).all()
    return render_template("internship/micro_bounties.html", bounties=bounties)

@internship_bp.route("/micro-bounties/<int:id>/submit", methods=["POST"])
@login_required
def submit_bounty(id):
    bounty = MicroProject.query.get_or_404(id)
    submission_url = request.form.get("submission_url")
    github_pr_url = request.form.get("github_pr_url")
    notes = request.form.get("notes")

    sub = MicroSubmission(
        project_id=bounty.id,
        student_id=current_user.id,
        submission_url=submission_url,
        github_pr_url=github_pr_url,
        notes=notes,
        status="submitted"
    )
    db.session.add(sub)
    db.session.commit()
    flash("Micro-Project Proof of Work submitted! The company will review your contribution.", "success")
    return redirect(url_for("internship.micro_bounties"))