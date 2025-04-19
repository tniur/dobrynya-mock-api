from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.get("/getServiceCategories")
def get_clinics(db: Session = Depends(get_db)):
    result = crud.get_all_service_categories(db)
    return {"data": result}