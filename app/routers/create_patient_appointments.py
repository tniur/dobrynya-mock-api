from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from datetime import datetime
from app.db import crud

router = APIRouter()

@router.post("/createAppointment")
def create_appointment(
    patient_key: str = Body(...),
    doctor_id: int = Body(...),
    clinic_id: int = Body(...),
    time_start: str = Body(...),  # "dd.mm.yyyy hh:mm"
    time_end: str = Body(...),    # "dd.mm.yyyy hh:mm"
    db: Session = Depends(get_db)
):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    try:
        dt_start = datetime.strptime(time_start, "%d.%m.%Y %H:%M")
        dt_end = datetime.strptime(time_end, "%d.%m.%Y %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use dd.mm.yyyy hh:mm")

    date_str = dt_start.strftime("%Y-%m-%d")
    time_str = f"{dt_start.strftime('%H:%M')} - {dt_end.strftime('%H:%M')}"
    time_start_str = dt_start.strftime("%Y-%m-%d %H:%M")
    time_end_str = dt_end.strftime("%Y-%m-%d %H:%M")
    created_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    appointment = crud.post_create_appointment(
        db=db,
        patient_id=patient_key_entry.patient_id,
        doctor_id=doctor_id,
        clinic_id=clinic_id,
        date=date_str,
        time=time_str,
        time_start=time_start_str,
        time_end=time_end_str,
        created=created_str,
        status="upcoming"
    )

    result = {
        "success": True,
        "appointment_id": appointment.id,
        "message": "Appointment successfully created"
    }
    return {"data": result}
