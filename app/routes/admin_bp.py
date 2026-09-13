from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User, Role
from app.models.internship import Internship
from app.models.application import Application
from app.models.system import AuditLog, Announcement
from app.services import security_service

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        flash("Unauthorized area. Administrator credentials required.", "danger")
        return redirect(url_for("auth.login"))

@admin_bp.route("/dashboard")
def dashboard():
    stats = {
        "total_users": User.query.count(),
        "students": User.query.filter_by(role=Role.STUDENT).count(),
        "companies": User.query.filter_by(role=Role.COMPANY).count(),
        "internships": Internship.query.count(),
        "applications": Application.query.count()
    }
    recent_users = User.query.order_by(User.created_at.desc()).limit(6).all()
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()

    return render_template("admin/dashboard.html", stats=stats, recent_users=recent_users, recent_logs=recent_logs, announcements=announcements)

@admin_bp.route("/users")
def manage_users():
    role_filter = request.args.get("role")
    query = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    users = query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users, selected_role=role_filter)

@admin_bp.route("/user/<int:id>/toggle-status", methods=["POST"])
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash("Cannot modify your own administrative status.", "warning")
        return redirect(url_for("admin.manage_users"))

    user.is_active = not user.is_active
    db.session.commit()
    security_service.log_action(current_user.id, "TOGGLE_USER_STATUS", "user", user.id, f"Set is_active={user.is_active}")
    flash(f"User {user.email} status updated to {'Active' if user.is_active else 'Suspended'}.", "info")
    return redirect(url_for("admin.manage_users"))

@admin_bp.route("/internships")
def manage_internships():
    internships = Internship.query.order_by(Internship.created_at.desc()).all()
    return render_template("admin/internships.html", internships=internships)

@admin_bp.route("/internship/<int:id>/toggle", methods=["POST"])
def toggle_internship(id):
    internship = Internship.query.get_or_404(id)
    internship.is_active = not internship.is_active
    db.session.commit()
    security_service.log_action(current_user.id, "MODERATE_INTERNSHIP", "internship", internship.id, f"Set active={internship.is_active}")
    flash(f"Internship '{internship.title}' status updated.", "success")
    return redirect(url_for("admin.manage_internships"))

@admin_bp.route("/announcements", methods=["GET", "POST"])
def announcements():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        target = request.form.get("target_role", "all")
        ann = Announcement(title=title, content=content, target_role=target)
        db.session.add(ann)
        db.session.commit()
        security_service.log_action(current_user.id, "POST_ANNOUNCEMENT", "announcement", ann.id, title)
        flash("Broadcast announcement published!", "success")
        return redirect(url_for("admin.announcements"))

    all_ann = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template("admin/announcements.html", announcements=all_ann)

@admin_bp.route("/audit-logs")
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(100).all()
    return render_template("admin/audit_logs.html", logs=logs)