from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.get("/getClinics")
def get_clinics(
    db: Session = Depends(get_db),
    accept_language: str = Header(default="en-US")
):
    lang = "en"
    if "ru-RU" in accept_language:
        lang = "ru-RU"

    clinics = crud.get_all_clinics(db)

    result = [
        {
            "id": clinic.id,
            "title": clinic.title_en if lang == "en" else clinic.title_ru,
            "doctor_name": clinic.doctor_name_en if lang == "en" else clinic.doctor_name_ru,
            "real_address": clinic.real_address_en if lang == "en" else clinic.real_address_ru,
            "phone": clinic.phone
        }
        for clinic in clinics
    ]
    return {"data": result}
