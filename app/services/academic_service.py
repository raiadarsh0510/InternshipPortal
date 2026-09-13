from datetime import datetime
from app.extensions import db
from app.models.academic import AcademicEvaluation
from app.models.application import Application

class AcademicService:
    @staticmethod
    def submit_evaluation(application_id, student_id, company_id, college_name, faculty_mentor_name, faculty_mentor_email, attendance, tech_comp, professionalism, proj_comp, remarks):
        existing = AcademicEvaluation.query.filter_by(application_id=application_id).first()
        if existing:
            eval_obj = existing
        else:
            eval_obj = AcademicEvaluation(
                application_id=application_id,
                student_id=student_id,
                company_id=company_id
            )
            db.session.add(eval_obj)

        eval_obj.college_name = college_name
        eval_obj.faculty_mentor_name = faculty_mentor_name
        eval_obj.faculty_mentor_email = faculty_mentor_email
        eval_obj.attendance_percentage = float(attendance)
        eval_obj.technical_competence = int(tech_comp)
        eval_obj.professionalism = int(professionalism)
        eval_obj.project_completion = int(proj_comp)
        
        # Calculate composite score (out of 10)
        composite = (int(tech_comp) * 0.4 + int(professionalism) * 0.2 + int(proj_comp) * 0.4) * 2.0
        eval_obj.overall_performance = round(composite, 1)

        # NEP 2020 Credit mapping (standard: 4 credits for 8-12 week full internship)
        eval_obj.nep_credits_awarded = 4 if composite >= 5.0 else 2
        
        if composite >= 9.0:
            eval_obj.grade = "O"
        elif composite >= 8.0:
            eval_obj.grade = "A+"
        elif composite >= 7.0:
            eval_obj.grade = "A"
        elif composite >= 6.0:
            eval_obj.grade = "B+"
        else:
            eval_obj.grade = "B"

        eval_obj.company_remarks = remarks
        eval_obj.is_verified_by_college = True
        eval_obj.verified_at = datetime.utcnow()
        db.session.commit()
        return eval_obj

academic_service = AcademicService()