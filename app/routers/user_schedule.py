from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.get("/getSchedule")
def get_user_schedule(
        clinic_id: int = Query(1),
        user_id: int = Query(...),
        db: Session = Depends(get_db)
):
    schedule = crud.get_user_schedule(db, user_id=user_id, clinic_id=clinic_id)

    result = [
        {
            "clinic_id": s.clinic_id,
            "date": s.date,
            "time_start": s.time_start,
            "time_start_short": s.time_start.split()[1] if s.time_start else "",
            "time_end": s.time_end,
            "time_end_short": s.time_end.split()[1] if s.time_end else "",
            "room": s.room,
            "is_busy": s.is_busy
        }
        for s in schedule
    ]
    return {"data": result}
