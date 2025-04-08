from sqlalchemy.orm import Session
from .models import Clinic, Profession

def get_all_clinics(db: Session):
    return db.query(Clinic).all()

def get_all_professions(db: Session):
    return db.query(Profession).all()