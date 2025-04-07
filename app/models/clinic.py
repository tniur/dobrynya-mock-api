from pydantic import BaseModel

class Clinic(BaseModel):
    id: int
    title: str
    doctor_name: str
    real_address: str
    phone: str
