from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient

router = APIRouter()

@router.post("/auth/recover/confirmCode")
def recover_confirm_code(
    email: str = Body(...),
    code: str = Body(...),
    db: Session = Depends(get_db)
):
    if code != "123456":
        raise HTTPException(status_code=401, detail="Invalid verification code")

    patient = db.query(Patient).filter(Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {
        "data": {
            "message": "Verification code confirmed"
        }
    }
