from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from datetime import datetime, timedelta
from app.db.models import User
import random

router = APIRouter()

@router.get("/getSchedule")
def get_user_schedule(
        clinic_id: int = Query(1),
        user_id: int = Query(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    clinic_ids = [clinic.id for clinic in user.clinics]
    if clinic_id not in clinic_ids:
        return {"data": []}

    today = datetime.now().date()
    room_number = random.randint(1, 300)

    result = []

    for day_offset in range(5):
        date = today + timedelta(days=day_offset)
        slots_count = random.randint(4, 10)
        start_hour = 9

        for slot in range(slots_count):
            time_start_dt = datetime.combine(date, datetime.min.time()) + timedelta(hours=start_hour + slot)
            time_end_dt = time_start_dt + timedelta(hours=1)

            time_start_str = time_start_dt.strftime("%Y-%m-%d %H:%M")
            time_end_str = time_end_dt.strftime("%Y-%m-%d %H:%M")
            time_start_short = time_start_dt.strftime("%H:%M")
            time_end_short = time_end_dt.strftime("%H:%M")

            result.append({
                "clinic_id": clinic_id,
                "date": date.strftime("%Y-%m-%d"),
                "time_start": time_start_str,
                "time_start_short": time_start_short,
                "time_end": time_end_str,
                "time_end_short": time_end_short,
                "room": str(room_number),
                "is_busy": False
            })

    return {"data": result}