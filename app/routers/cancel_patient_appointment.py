from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud

router = APIRouter()

@router.post("/cancelAppointment")
def cancel_appointment(
    appointment_id: int = Body(...),
    db: Session = Depends(get_db)
):
    try:
        updated = crud.cancel_appointment(db, appointment_id=appointment_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "success": True,
        "appointment_id": updated.id,
        "status": updated.status,
        "message": "Appointment cancelled"
    }