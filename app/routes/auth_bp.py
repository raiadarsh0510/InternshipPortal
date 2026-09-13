from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.services import auth_service, security_service, notification_service
from app.forms import LoginForm, StudentRegisterForm, CompanyRegisterForm
from app.models.user import Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_role_dashboard(current_user)

    form = LoginForm()
    if form.validate_on_submit():
        user = auth_service.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            security_service.log_action(user.id, "USER_LOGIN", "user", user.id, "User logged in successfully")
            flash(f"Welcome back to TELEPORTAL, {user.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect_role_dashboard(user)
        else:
            flash("Invalid email or password. Please check your credentials.", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect_role_dashboard(current_user)

    role_type = request.args.get("role", "student")
    student_form = StudentRegisterForm()
    company_form = CompanyRegisterForm()

    if request.method == "POST":
        if role_type == "company" and company_form.validate_on_submit():
            user, err = auth_service.register_company(
                company_name=company_form.company_name.data,
                hr_name=company_form.hr_name.data,
                email=company_form.email.data,
                password=company_form.password.data,
                location=company_form.location.data,
                website=company_form.website.data
            )
            if user:
                login_user(user)
                security_service.log_action(user.id, "COMPANY_REGISTER", "user", user.id, f"Registered company: {company_form.company_name.data}")
                flash("Company account created successfully! Welcome to TELEPORTAL.", "success")
                return redirect(url_for("company.dashboard"))
            flash(err, "danger")

        elif student_form.validate_on_submit():
            user, err = auth_service.register_student(
                name=student_form.name.data,
                email=student_form.email.data,
                password=student_form.password.data,
                phone=student_form.phone.data,
                college=student_form.college.data,
                branch=student_form.branch.data
            )
            if user:
                login_user(user)
                security_service.log_action(user.id, "STUDENT_REGISTER", "user", user.id, "Registered new student account")
                flash("Account created successfully! Start exploring internships.", "success")
                return redirect(url_for("student.dashboard"))
            flash(err, "danger")

    return render_template("auth/register.html", student_form=student_form, company_form=company_form, role_type=role_type)

@auth_bp.route("/logout")
@login_required
def logout():
    security_service.log_action(current_user.id, "USER_LOGOUT", "user", current_user.id, "User logged out")
    logout_user()
    flash("You have been signed out safely. See you soon!", "info")
    return redirect(url_for("auth.login"))

def redirect_role_dashboard(user):
    if user.role in [Role.ADMIN, Role.SUPER_ADMIN]:
        return redirect(url_for("admin.dashboard"))
    elif user.role == Role.COMPANY:
        return redirect(url_for("company.dashboard"))
    return redirect(url_for("student.dashboard"))