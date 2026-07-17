import re

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from app.models import User
from app.utils import send_verification_email, confirm_verification_token


def init_auth_routes(app):

    # ---------------- LOGIN ---------------- #

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"].strip().lower()
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):

                if not user.email_verified:
                    flash(
                        "Please verify your email address before logging in.",
                        "warning"
                    )
                    return render_template("login.html")

                login_user(user, remember=True)

                flash("Login Successful!", "success")

                return redirect(url_for("dashboard"))

            flash("Invalid Email or Password", "danger")

            return render_template("login.html")

        return render_template("login.html")

    # ---------------- REGISTER ---------------- #

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            role = request.form["role"]

            # Password Validation

            if len(password) < 8:
                flash("Password must be at least 8 characters long.", "danger")
                return redirect(url_for("register"))

            if not re.search(r"[A-Z]", password):
                flash("Password must contain at least one uppercase letter.", "danger")
                return redirect(url_for("register"))

            if not re.search(r"[a-z]", password):
                flash("Password must contain at least one lowercase letter.", "danger")
                return redirect(url_for("register"))

            if not re.search(r"\d", password):
                flash("Password must contain at least one digit.", "danger")
                return redirect(url_for("register"))

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                flash("Password must contain at least one special character.", "danger")
                return redirect(url_for("register"))

            # Check Existing Email

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                flash("Email already registered.", "warning")
                return redirect(url_for("register"))

            # Hash Password

            hashed_password = generate_password_hash(password)

            new_user = User(
                name=name,
                email=email,
                password=hashed_password,
                role=role,
                email_verified=False
            )

            db.session.add(new_user)
            db.session.commit()

            send_verification_email(new_user)

            flash("Registration successful! Please check your email to verify your account.", "success")

            return redirect(url_for("login"))

        return render_template("register.html")

    # ---------------- LOGOUT ---------------- #

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash("Logged out successfully.", "success")

        return redirect(url_for("login"))

    # ---------------- EMAIL VERIFICATION ---------------- #

    @app.route("/verify_email/<token>")
    def verify_email(token):

        try:
            email = confirm_verification_token(token)
        except Exception:
            flash("Invalid or expired verification link.", "danger")
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("User not found.", "danger")
            return redirect(url_for("login"))

        if user.email_verified:
            flash("Email already verified.", "info")
            return redirect(url_for("login"))

        user.email_verified = True
        db.session.commit()

        flash("Email verified successfully! You can now login.", "success")
        return redirect(url_for("login"))