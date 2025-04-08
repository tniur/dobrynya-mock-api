from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Clinic, Profession, User, ServiceCategories

def get_all_clinics(db: Session):
    return db.query(Clinic).all()

def get_all_professions(db: Session):
    return db.query(Profession).all()

def get_all_users(
    db: Session,
    user_ids: Optional[List[int]] = None,
    clinic_id: Optional[int] = None,
    profession_id: Optional[int] = None,
):
    query = db.query(User)

    if user_ids:
        query = query.filter(User.id.in_(user_ids))
    if clinic_id:
        query = query.filter(User.clinics.any(Clinic.id == clinic_id))
    if profession_id:
        query = query.filter(User.professions.any(Profession.id == profession_id))

    return query.all()

def get_all_service_categories(db: Session):
    return db.query(ServiceCategories).all()