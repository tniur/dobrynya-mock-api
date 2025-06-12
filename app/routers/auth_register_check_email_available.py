from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient

router = APIRouter()

@router.post("/register/checkEmailAvailable")
def check_email_available(
    email: str = Body(...),
    db: Session = Depends(get_db)
):
    existing_patient = db.query(Patient).filter(Patient.email == email).first()
    if existing_patient:
        raise HTTPException(status_code=409, detail="Email already registered")

    return {"data": {"message": "Email is available"}}
