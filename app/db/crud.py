from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Clinic, Profession, User, ServiceCategories, Service

def get_all_clinics(db: Session):
    return db.query(Clinic).all()

def get_all_professions(db: Session):
    return db.query(Profession).all()

def get_filtered_users(
    db: Session,
    user_ids: Optional[List[int]] = None,
    clinic_id: Optional[int] = None,
    profession_id: Optional[int] = None,
    service_ids: Optional[List[int]] = None,
):
    query = db.query(User)

    if user_ids:
        query = query.filter(User.id.in_(user_ids))
    if clinic_id:
        query = query.filter(User.clinics.any(Clinic.id == clinic_id))
    if profession_id:
        query = query.filter(User.professions.any(Profession.id == profession_id))
    if service_ids:
        query = query.join(User.services).filter(Service.id.in_(service_ids))

    return query.all()

def get_all_service_categories(db: Session):
    return db.query(ServiceCategories).all()

def get_filtered_services(
    db: Session,
    service_ids: Optional[List[int]] = None,
    profession_id: Optional[int] = None,
    category_ids: Optional[List[int]] = None,
):
    query = db.query(Service)

    if service_ids:
        query = query.filter(Service.id.in_(service_ids))
    if profession_id:
        query = query.filter(Service.profession_id == profession_id)
    if category_ids:
        query = query.join(Service.category_ids).filter(ServiceCategories.id.in_(category_ids))

    return query.all()