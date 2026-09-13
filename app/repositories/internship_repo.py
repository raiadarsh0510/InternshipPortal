from app.repositories.base import BaseRepository
from app.models.internship import Internship, Category, MicroProject
from app.extensions import db
from datetime import date

class InternshipRepository(BaseRepository):
    def __init__(self):
        super().__init__(Internship)

    def search_internships(self, keyword=None, category_id=None, location=None, internship_type=None, min_stipend=None, remote_only=False):
        query = Internship.query.filter(Internship.is_active == True, Internship.deadline >= date.today())
        
        if keyword:
            term = f"%{keyword.strip()}%"
            query = query.filter(
                (Internship.title.ilike(term)) |
                (Internship.description.ilike(term)) |
                (Internship.skills.ilike(term))
            )
        if category_id:
            query = query.filter(Internship.category_id == category_id)
        if location:
            query = query.filter(Internship.location.ilike(f"%{location.strip()}%"))
        if internship_type:
            query = query.filter(Internship.internship_type == internship_type)
        if min_stipend is not None and min_stipend > 0:
            query = query.filter(Internship.stipend_amount >= min_stipend)
        if remote_only:
            query = query.filter(Internship.internship_type.ilike("%Virtual%") | Internship.internship_type.ilike("%Remote%"))
            
        return query.order_by(Internship.created_at.desc())

    def get_featured(self, limit=6):
        return Internship.query.filter_by(is_active=True, is_featured=True).limit(limit).all()

    def get_by_company(self, company_id):
        return Internship.query.filter_by(company_id=company_id).order_by(Internship.created_at.desc()).all()