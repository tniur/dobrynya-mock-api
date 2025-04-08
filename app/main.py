from fastapi import FastAPI
from app.routers import clinics, professions, users

app = FastAPI(title="Mock DobrynyaNN API")

app.include_router(clinics.router, tags=["Clinics"])
app.include_router(professions.router, tags=["Professions"])
app.include_router(users.router, tags=["Users"])
