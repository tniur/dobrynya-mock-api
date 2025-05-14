from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_filtered_users

router = APIRouter()

@router.get("/getUsers")
def get_users(
    user_id: Optional[str] = None,
    clinic_id: Optional[int] = None,
    profession_id: Optional[int] = None,
    service_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    user_ids = [int(x) for x in user_id.split(",")] if user_id else None
    service_ids = [int(x) for x in service_id.split(",")] if service_id else None

    users = get_filtered_users(
        db,
        user_ids=user_ids,
        clinic_id=clinic_id,
        profession_id=profession_id,
        service_ids=service_ids
    )

    result = []
    for user in users:
        avatar_path = None
        if user.avatar_path:
            avatar_path = f"/static/{user.avatar_path}"

        avatar_small_path = None
        if user.avatar_small_path:
            avatar_small_path = f"/static/{user.avatar_small_path}"

        professions = user.professions
        profession_ids = [p.id for p in professions]
        professions_title = ", ".join(p.doctor_name.lower() for p in professions if p.doctor_name)

        result.append({
            "id": user.id,
            "avatar_path": avatar_path,
            "avatar_small_path": avatar_small_path,
            "name": user.name,
            "birth_date": user.birth_date,
            "gender": user.gender,
            "phone": user.phone,
            "email": user.email,
            "profession_ids": profession_ids,
            "professions_title": professions_title,
            "clinic": [c.id for c in user.clinics],
            "services": [s.id for s in user.services],
        })

    return {"data": result}
