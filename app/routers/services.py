from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.crud import get_filtered_services

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/getServices")
def get_services(
    service_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service_ids = [int(x) for x in service_id.split(",")] if service_id else None

    services = get_filtered_services(
        db,
        service_ids=service_ids,
    )

    result = []
    for service in services:
        result.append({
            "id": service.id,
            "title": service.title,
            "price": service.price,
            "duration": service.duration,
            "short_desc": service.short_desc,
            "full_desc": service.full_desc,
        })

    return result