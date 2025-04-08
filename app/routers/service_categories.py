from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/getServiceCategories")
def get_clinics(db: Session = Depends(get_db)):
    return crud.get_all_service_categories(db)