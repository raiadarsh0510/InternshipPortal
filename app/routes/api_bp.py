from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.extensions import db
from app.models.system import Notification
from app.models.internship import Internship

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/notifications/unread")
@login_required
def unread_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(10).all()
    return jsonify({
        "count": len(notifs),
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "link": n.link or "#",
                "time": n.created_at.strftime("%b %d, %I:%M %p")
            }
            for n in notifs
        ]
    })

@api_bp.route("/notifications/<int:id>/mark-read", methods=["POST"])
@login_required
def mark_notification_read(id):
    notif = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    notif.is_read = True
    db.session.commit()
    return jsonify({"success": True})

@api_bp.route("/search/live")
def live_search():
    q = request.args.get("q", "").strip()
    if len(q) < 2:
        return jsonify([])
    matches = Internship.query.filter(
        Internship.is_active == True,
        (Internship.title.ilike(f"%{q}%")) | (Internship.skills.ilike(f"%{q}%"))
    ).limit(5).all()
    return jsonify([
        {"id": m.id, "title": m.title, "company": m.company_user.company_profile.company_name if m.company_user and m.company_user.company_profile else "Verified Partner", "location": m.location, "stipend": m.stipend_amount}
        for m in matches
    ])