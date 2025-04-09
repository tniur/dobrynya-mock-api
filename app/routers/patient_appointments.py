from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from app.db import crud

router = APIRouter()

@router.get("/getPatientAppointments")
def get_patient_appointments(patient_key: str = Query(...), db: Session = Depends(get_db)):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    appointments = crud.get_appointments_by_patient(db, patient_key_entry.patient_id)

    return [
        {
            "appointment_id": a.id,
            "date": a.date,
            "time": a.time,
            "time_start": a.time_start,
            "time_end": a.time_end,
            "clinic_id": a.clinic_id,
            "doctor_id": a.doctor_id,
            "created": a.created,
            "status": a.status
        }
        for a in appointments
    ]