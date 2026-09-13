from datetime import datetime
from app.extensions import db
from app.models.internship import Internship, Category, MicroProject, MicroSubmission
from app.models.application import Application, SavedInternship
from app.repositories import internship_repo

class InternshipService:
    @staticmethod
    def create_internship(company_id, title, category_id, internship_type, location, stipend_type, stipend_amount, duration_weeks, openings, description, responsibilities, requirements, skills, benefits, deadline):
        slug = f"{title.lower().replace(' ', '-')[:120]}-{int(datetime.utcnow().timestamp())}"
        internship = Internship(
            company_id=company_id,
            title=title.strip(),
            slug=slug,
            category_id=category_id,
            internship_type=internship_type,
            location=location.strip(),
            stipend_type=stipend_type,
            stipend_amount=stipend_amount,
            duration_weeks=duration_weeks,
            openings=openings,
            description=description,
            responsibilities=responsibilities,
            requirements=requirements,
            skills=skills,
            benefits=benefits,
            deadline=deadline
        )
        db.session.add(internship)
        db.session.commit()
        return internship

    @staticmethod
    def calculate_match_score(student_skills_list, internship_skills_str):
        if not student_skills_list or not internship_skills_str:
            return 50 # Baseline
        job_skills = [s.strip().lower() for s in internship_skills_str.split(",") if s.strip()]
        if not job_skills:
            return 60
        student_skills_lower = [s.lower() for s in student_skills_list]
        matched = [s for s in job_skills if any(s in st or st in s for st in student_skills_lower)]
        score = int((len(matched) / len(job_skills)) * 100)
        return max(min(score, 100), 20)

    @staticmethod
    def toggle_save_internship(student_id, internship_id):
        saved = SavedInternship.query.filter_by(student_id=student_id, internship_id=internship_id).first()
        if saved:
            db.session.delete(saved)
            db.session.commit()
            return False # Removed
        else:
            new_save = SavedInternship(student_id=student_id, internship_id=internship_id)
            db.session.add(new_save)
            db.session.commit()
            return True # Saved

internship_service = InternshipService()