from fastapi import APIRouter
from app.models.profession import Profession
import json
from pathlib import Path

router = APIRouter()

@router.get("/", response_model=list[Profession])
def get_professions():
    professions_path = Path(__file__).resolve().parent.parent / "data" / "professions.json"
    with open(professions_path, "r", encoding="utf-8") as f:
        professions = json.load(f)
    return professions
