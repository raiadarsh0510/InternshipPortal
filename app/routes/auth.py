import re

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db
from app.models import User


def init_auth_routes(app):

    # ---------------- LOGIN ---------------- #

    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            email = request.form["email"]
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):

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
                role=role
            )

            db.session.add(new_user)
            db.session.commit()

            flash("Registration Successful! Please Login.", "success")

            return redirect(url_for("login"))

        return render_template("register.html")

    # ---------------- LOGOUT ---------------- #

    @app.route("/logout")
    @login_required
    def logout():

        logout_user()

        flash("Logged out successfully.", "success")

        return redirect(url_for("login"))