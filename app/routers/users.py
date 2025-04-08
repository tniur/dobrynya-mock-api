from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import get_all_users

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/getUsers")
def get_users(
    user_id: Optional[str] = None,
    clinic_id: Optional[int] = None,
    profession_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    user_ids = [int(x) for x in user_id.split(",")] if user_id else None

    users = get_all_users(
        db,
        user_ids=user_ids,
        clinic_id=clinic_id,
        profession_id=profession_id,
    )

    result = []
    for user in users:
        result.append({
            "id": user.id,
            "avatar": user.avatar,
            "avatar_small": user.avatar_small,
            "name": user.name,
            "birth_date": user.birth_date,
            "gender": user.gender,
            "phone": user.phone,
            "email": user.email,
            "profession": [p.id for p in user.professions],
            "clinic": [c.id for c in user.clinics],
        })

    return result
