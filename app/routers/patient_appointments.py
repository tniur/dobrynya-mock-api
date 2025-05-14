from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey, User, Clinic, Service
from app.db import crud

router = APIRouter()

@router.get("/getPatientAppointments")
def get_patient_appointments(
        patient_key: str = Query(...),
        appointment_id: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    all_appointments = crud.get_appointments_by_patient(db, patient_key_entry.patient_id)
    appointment_ids = [int(x) for x in appointment_id.split(",")] if appointment_id else None
    appointments = [a for a in all_appointments if not appointment_ids or a.id in appointment_ids]

    result = []

    for appointment in appointments:
        doctor = db.query(User).filter_by(id=appointment.doctor_id).first()
        doctor_name = doctor.name

        clinic = db.query(Clinic).filter_by(id=appointment.clinic_id).first()
        clinic_address = clinic.real_address

        service = db.query(Service).filter_by(id=appointment.service_id).first()
        service_name = service.title

        result.append({
                "appointment_id": appointment.id,
                "date": appointment.date,
                "time": appointment.time,
                "time_start": appointment.time_start,
                "time_end": appointment.time_end,
                "clinic_id": appointment.clinic_id,
                "clinic_address": clinic_address,
                "doctor_id": appointment.doctor_id,
                "doctor_name": doctor_name,
                "service_id": appointment.service_id,
                "service_name": service_name,
                "created": appointment.created,
                "status": appointment.status
        })

    return {"data": result}