from pydantic import BaseModel

class Profession(BaseModel):
    id: int
    name: str
    doctor_name: str
    is_deleted: bool
