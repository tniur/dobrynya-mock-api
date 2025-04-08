from typing import List, Optional
from pydantic import BaseModel
from .clinic import Clinic
from .profession import Profession

class User(BaseModel):
    id: int
    avatar: Optional[str] = None
    avatar_small: Optional[str] = None
    name: str
    birth_date: str
    gender: str
    phone: str
    email: str
    clinics: List[Clinic] = []
    professions: List[Profession] = []