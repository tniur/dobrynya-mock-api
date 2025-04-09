from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.get("/getClinics")
def get_clinics(db: Session = Depends(get_db)):
    return crud.get_all_clinics(db)
