from datetime import date
import os
from werkzeug.utils import secure_filename

from datetime import datetime

from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user

from app.database import db
from app.models import Internship


def init_internship_routes(app):

    # ==========================================
    # View Internships
    # ==========================================
    @app.route("/internships")
    @login_required
    def internships():

        search = request.args.get("search", "").strip()
        location = request.args.get("location", "").strip()
        stipend = request.args.get("stipend", "").strip()
        sort = request.args.get("sort", "newest")

        # Create base query FIRST
        if current_user.role.lower() == "company":

            query = Internship.query.filter_by(
                posted_by=current_user.id
            )

        else:

            query = Internship.query

        # Search
        if search:

            query = query.filter(
                (Internship.title.ilike(f"%{search}%")) |
                (Internship.company.ilike(f"%{search}%")) |
                (Internship.skills.ilike(f"%{search}%"))
            )

        # Location
        if location:

            query = query.filter(
                Internship.location.ilike(f"%{location}%")
            )

        # Sorting
        if stipend:
            query = query.filter(
                Internship.stipend >= int(stipend)
            )
            
        elif sort == "highest":

            query = query.order_by(
                Internship.stipend.desc()
            )    

        elif sort == "lowest":

            query = query.order_by(
                Internship.stipend.asc()
            )

        elif sort == "company":

            query = query.order_by(
                Internship.company.asc()
            )

        elif sort == "deadline":

            query = query.order_by(
                Internship.last_date.asc()
            )

        else:

            query = query.order_by(
                Internship.id.desc()
            )

        internships = query.all()

        return render_template(
            "internships.html",
            internships=internships,
            search=search,
            stipend=stipend,
            location=location,
            today=date.today(),
            sort=sort
        )

    # ==========================================
    # Add Internship
    # ==========================================
    @app.route("/add_internship", methods=["GET", "POST"])
    @login_required
    def add_internship():

        if current_user.role.lower() != "company":

            flash(
                "Only companies can post internships.",
                "danger"
            )

            return redirect(url_for("dashboard"))

        if request.method == "POST":
            
            logo = request.files.get("company_logo")

            logo_name = None

            if logo and logo.filename != "":

                logo_name = secure_filename(logo.filename)

                logo.save(

                    os.path.join(

                        "static",

                        "images",

                        "company_logos",

                        logo_name

                    )

                )

            category = request.form.get("category")

            internship_type = request.form.get("internship_type")

            experience = request.form.get("experience")

            responsibilities = request.form.get("responsibilities")

            requirements = request.form.get("requirements")

            benefits = request.form.get("benefits")

            internship = Internship(

                title=request.form["title"].strip(),

                company=request.form["company"].strip(),
                
                category=category,
                
                internship_type=internship_type,
                
                
                
                experience=request.form.get("experience", "").strip(),
                
                responsibilities=responsibilities,
                
                requirements=requirements,
                
                benefits=benefits,

                location=request.form["location"].strip(),

                stipend=int(request.form["stipend"])
                if request.form["stipend"]
                else None,

                duration=request.form["duration"].strip(),

                skills=request.form["skills"].strip(),

                description=request.form["description"].strip(),

                last_date=datetime.strptime(
                    request.form["last_date"],
                    "%Y-%m-%d"
                ).date(),
                
                company_logo=logo_name,

                posted_by=current_user.id
            )

            db.session.add(internship)
            db.session.commit()

            flash(
                "Internship Added Successfully!",
                "success"
            )

            return redirect(url_for("internships"))

        return render_template(
            "add_internship.html"
        )

    # ==========================================
    # Edit Internship
    # ==========================================
    @app.route(
        "/edit_internship/<int:internship_id>",
        methods=["GET", "POST"]
    )
    @login_required
    def edit_internship(internship_id):

        internship = Internship.query.get_or_404(
            internship_id
        )

        if internship.posted_by != current_user.id:

            flash(
                "You are not authorized.",
                "danger"
            )

            return redirect(
                url_for("internships")
            )

        if request.method == "POST":

            internship.title = request.form[
                "title"
            ].strip()

            internship.company = request.form[
                "company"
            ].strip()

            internship.location = request.form[
                "location"
            ].strip()
            
            internship.category = request.form.get("category", "").strip()

            internship.internship_type = request.form.get("internship_type", "").strip()

            internship.experience = request.form.get("experience", "").strip()

            internship.responsibilities = request.form.get("responsibilities", "").strip()

            internship.requirements = request.form.get("requirements", "").strip()

            internship.benefits = request.form.get("benefits", "").strip()

            internship.stipend = (
                int(request.form["stipend"])
                if request.form["stipend"]
                else None
            )

            internship.duration = request.form[
                "duration"
            ].strip()

            internship.skills = request.form[
                "skills"
            ].strip()

            internship.description = request.form[
                "description"
            ].strip()
            
            

            internship.last_date = datetime.strptime(
                request.form["last_date"],
                "%Y-%m-%d"
            ).date()
            
            logo = request.files.get("company_logo")

            if logo and logo.filename != "":

                logo_name = secure_filename(logo.filename)

                logo.save(
                    os.path.join(
                        "static",
                        "images",
                        "company_logos",
                        logo_name
                    )
                )

                internship.company_logo = logo_name

            db.session.commit()

            flash(
                "Internship Updated Successfully!",
                "success"
            )

            return redirect(
                url_for("internships")
            )

        return render_template(
            "edit_internship.html",
            internship=internship
        )

    # ==========================================
    # Delete Internship
    # ==========================================
    @app.route(
        "/delete_internship/<int:internship_id>"
    )
    @login_required
    def delete_internship(internship_id):

        internship = Internship.query.get_or_404(
            internship_id
        )

        if internship.posted_by != current_user.id:

            flash(
                "You are not authorized.",
                "danger"
            )

            return redirect(
                url_for("internships")
            )

        db.session.delete(internship)

        db.session.commit()

        flash(
            "Internship Deleted Successfully!",
            "success"
        )

        return redirect(
            url_for("internships")
        )
    
    # ==========================================
    # Apply Internship
    # ==========================================
        
    @app.route("/apply/<int:internship_id>")
    @login_required
    def apply_internship(internship_id):

        from app.models import Application
        from datetime import date

        if current_user.role.lower() != "student":

            flash(
                "Only students can apply for internships.",
                "danger"
            )

            return redirect(url_for("internships"))

        internship = Internship.query.get_or_404(
            internship_id
        )

        # Check if internship has expired
        if internship.last_date < date.today():

            flash(
                "This internship has expired.",
                "danger"
            )

            return redirect(url_for("internships"))

        existing = Application.query.filter_by(
            internship_id=internship.id,
            student_id=current_user.id
        ).first()

        if existing:

            flash(
                "You have already applied.",
                "warning"
            )

            return redirect(url_for("internships"))

        application = Application(
            internship_id=internship.id,
            student_id=current_user.id,
            status="Pending"
        )

        db.session.add(application)
        db.session.commit()

        flash(
            "Application Submitted Successfully!",
            "success"
        )

        return redirect(url_for("internships"))
    
    # ==========================================
    # Save Internship
    # ==========================================
    @app.route("/save/<int:internship_id>")
    @login_required
    def save_internship(internship_id):

        from app.models import SavedInternship

        if current_user.role.lower() != "student":
            flash("Only students can save internships.", "danger")
            return redirect(url_for("internships"))

        internship = Internship.query.get_or_404(internship_id)

        existing = SavedInternship.query.filter_by(
            student_id=current_user.id,
            internship_id=internship.id
        ).first()

        if existing:
            flash("Internship already saved.", "warning")
            return redirect(url_for("internships"))

        saved = SavedInternship(
            student_id=current_user.id,
            internship_id=internship.id
        )

        db.session.add(saved)
        db.session.commit()

        flash("Internship saved successfully!", "success")

        return redirect(url_for("internships"))
    
    # ==========================================
    # Saved Internships
    # ==========================================
    @app.route("/saved_internships")
    @login_required
    def saved_internships():

        from app.models import SavedInternship

        saved = SavedInternship.query.filter_by(
            student_id=current_user.id
        ).all()

        internship_data = []

        for item in saved:

            internship = Internship.query.get(item.internship_id)

            if internship:

                internship_data.append(internship)

            return render_template(
                "saved_internships.html",
                internships=internship_data
            )
    
    # ==========================================
    # View Applicants
    # ==========================================
    @app.route("/applicants/<int:internship_id>")
    @login_required
    def view_applicants(internship_id):

        from app.models import Application, User

        internship = Internship.query.get_or_404(
            internship_id
        )
        
        if current_user.role.lower() != "company":
            
            flash(
                "Only companies can view applicants.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )

        if internship.posted_by != current_user.id:

            flash(
                "Unauthorized Access.",
                "danger"
            )

            return redirect(
                url_for("internships")
            )

        applications = db.session.query(
            Application,
            User
        ).join(
            User,
            Application.student_id == User.id
        ).filter(
            Application.internship_id == internship.id
        ).all()

        return render_template(
            "view_applicants.html",
            internship=internship,
            applications=applications
        )

    # ==========================================
    # Accept Application
    # ==========================================
    @app.route("/accept_application/<int:application_id>")
    @login_required
    def accept_application(application_id):

        from app.models import Application

        application = Application.query.get_or_404(
            application_id
        )

        internship = Internship.query.get_or_404(
            application.internship_id
        )

        if internship.posted_by != current_user.id:

            flash(
                "Unauthorized!",
                "danger"
            )

            return redirect(
                url_for("internships")
            )

        application.status = "Accepted"

        db.session.commit()

        flash(
            "Application Accepted!",
            "success"
        )

        return redirect(
            url_for(
                "view_applicants",
                internship_id=internship.id
            )
        )

    # ==========================================
    # Reject Application
    # ==========================================
    @app.route("/reject_application/<int:application_id>")
    @login_required
    def reject_application(application_id):

        from app.models import Application

        application = Application.query.get_or_404(
            application_id
        )

        internship = Internship.query.get_or_404(
            application.internship_id
        )

        if internship.posted_by != current_user.id:

            flash(
                "Unauthorized!",
                "danger"
            )

            return redirect(
                url_for("internships")
            )

        application.status = "Rejected"

        db.session.commit()

        flash(
            "Application Rejected!",
            "success"
        )

        return redirect(
            url_for(
                "view_applicants",
                internship_id=internship.id
            )
        )
        
    # ==========================================
    # My Applications
    # ==========================================
    @app.route("/my_applications")
    @login_required
    def my_applications():

        from app.models import Application

        if current_user.role.lower() != "student":

            flash(
                "Only students can access this page.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )

        applications = Application.query.filter_by(
            student_id=current_user.id
        ).all()

        application_data = []

        for application in applications:

            internship = Internship.query.get(
                application.internship_id
            )

            if internship:

                application_data.append({

                    "id": application.id,

                    "internship_id": internship.id,

                    "title": internship.title,

                    "company": internship.company,

                    "company_logo": internship.company_logo,

                    "location": internship.location,

                    "stipend": internship.stipend,

                    "duration": internship.duration,

                    "status": application.status

                })

        return render_template(

            "my_applications.html",

            application_data=application_data

        )


    # ==========================================
    # Delete / Withdraw Application
    # ==========================================
    @app.route("/delete_application/<int:application_id>")
    @login_required
    def delete_application(application_id):

        from app.models import Application

        application = Application.query.get_or_404(
            application_id
        )

        if application.student_id != current_user.id:

            flash(
                "Unauthorized!",
                "danger"
            )

            return redirect(
                url_for("my_applications")
            )

        db.session.delete(application)
        db.session.commit()

        flash(
            "Application Withdrawn Successfully!",
            "success"
        )

        return redirect(
            url_for("my_applications")
        )


    # ==========================================
    # Internship Details
    # ==========================================
    @app.route("/internship/<int:internship_id>")
    @login_required
    def internship_details(internship_id):
        
        from datetime import date

        internship = Internship.query.get_or_404(
            internship_id
        )

        return render_template(
            "internship_details.html",
            internship=internship,
            today=date.today()
        )

    print("✅ All Internship Routes Registered Successfully")               