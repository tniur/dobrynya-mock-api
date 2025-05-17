from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient
from pydantic import BaseModel

router = APIRouter()

class RegisterRequest(BaseModel):
    email: str
    password: str
    mobile: str

@router.post("/auth/register/requestCode")
def register_request_code(
    req: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing_patient = db.query(Patient).filter(Patient.email == req.email).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "data": {
            "message": "Verification code sent",
            "phone": req.mobile
        }
    }
