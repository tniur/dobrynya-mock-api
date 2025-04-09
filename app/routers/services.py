from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_filtered_services

router = APIRouter()

@router.get("/getServices")
def get_services(
    service_id: Optional[str] = None,
    profession_id: Optional[int] = None,
    category_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service_ids = [int(x) for x in service_id.split(",")] if service_id else None
    category_ids = [int(x) for x in category_id.split(",")] if category_id else None

    services = get_filtered_services(
        db,
        profession_id=profession_id,
        service_ids=service_ids,
        category_ids=category_ids
    )

    result = []
    for service in services:
        result.append({
            "id": service.id,
            "title": service.title,
            "price": service.price,
            "duration": service.duration,
            "profession_id": service.profession_id,
            "category_id": [c.id for c in service.category_ids],
            "short_desc": service.short_desc,
            "full_desc": service.full_desc,
        })

    return result
