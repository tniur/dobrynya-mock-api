from fastapi import APIRouter
from app.models.clinic import Clinic
import json
from pathlib import Path

router = APIRouter()

@router.get("/", response_model=list[Clinic])
def get_clinics():
    with open(Path("app/data/clinics.json"), "r", encoding="utf-8") as f:
        clinics = json.load(f)
    return clinics
