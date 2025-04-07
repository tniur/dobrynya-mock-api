from fastapi import FastAPI
from app.routers import clinics, professions

app = FastAPI(title="Mock DobrynyaNN API")

app.include_router(clinics.router, prefix="/clinics", tags=["Clinics"])
app.include_router(professions.router, prefix="/professions", tags=["Professions"])
