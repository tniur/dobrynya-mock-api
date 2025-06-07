from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.get("/getServiceCategories")
def get_service_categories(
    db: Session = Depends(get_db),
    accept_language: str = Header(default="ru")
):
    categories = crud.get_all_service_categories(db)

    lang = "ru"
    if "en" in accept_language:
        lang = "en"

    result = [
        {
            "id": cat.id,
            "title": cat.title_en if lang == "en" else cat.title_ru
        }
        for cat in categories
    ]
    return {"data": result}
