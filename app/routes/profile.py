import os
from werkzeug.utils import secure_filename

from app.models import User
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from app.database import db


def init_profile_routes(app):

    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():

        if request.method == "POST":
            
            profile_image = request.files.get("profile_image")

            if profile_image and profile_image.filename != "":

                allowed = (".jpg", ".jpeg", ".png")

                if profile_image.filename.lower().endswith(allowed):

                    image_name = secure_filename(profile_image.filename)

                    profile_image.save(
                        os.path.join(
                            "static",
                            "images",
                            "profiles",
                             image_name
                        )
                    )

                    current_user.profile_image = image_name

                else:

                    flash("Only JPG, JPEG and PNG images are allowed.", "danger")

                    return render_template("profile.html")

            phone = request.form.get("phone", "").strip()

            if not phone.isdigit() or len(phone) != 10:
                flash("Phone number must contain exactly 10 digits.", "danger")
                return render_template("profile.html")

            current_user.name = request.form.get("name", "").strip()
            new_email = request.form.get("email", "").strip().lower()

            existing_user = User.query.filter_by(email=new_email).first()

            if existing_user and existing_user.id != current_user.id:

                flash(
                    "This email is already registered.",
                    "danger"
                )

                return render_template("profile.html")

            current_user.email = new_email
            current_user.phone = request.form.get("phone", "").strip()
            current_user.college = request.form.get("college", "").strip()
            current_user.branch = request.form.get("branch", "").strip()
            current_user.year = request.form.get("year", "").strip()
            current_user.skills = request.form.get("skills", "").strip()
            current_user.bio = request.form.get("bio", "").strip()
            
            resume = request.files.get("resume")

            if resume and resume.filename != "":

                if not resume.filename.lower().endswith(".pdf"):

                    flash(
                        "Only PDF files are allowed.",
                        "danger"
                    )

                    return render_template("profile.html")

                filename = secure_filename(resume.filename)

                resume.save(
                    os.path.join(
                        "static",
                        "resumes",
                        filename
                    )
                )

                current_user.resume = filename

            db.session.commit()

            flash("Profile updated successfully!", "success")

            return redirect(url_for("profile"))

        return render_template("profile.html")
    
    @app.route("/student/<int:student_id>")
    @login_required
    def student_profile(student_id):

        from app.models import User

        if current_user.role.lower() != "company":
            flash("Unauthorized!", "danger")
            return redirect(url_for("dashboard"))

        student = User.query.get_or_404(student_id)

        return render_template(
            "student_profile.html",
            student=student
        )