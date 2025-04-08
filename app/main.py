from fastapi import FastAPI
from app.routers import clinics, professions, users, service_categories

app = FastAPI(title="Mock DobrynyaNN API")

app.include_router(clinics.router, tags=["Clinics"])
app.include_router(professions.router, tags=["Professions"])
app.include_router(users.router, tags=["Users"])
app.include_router(service_categories.router, tags=["ServiceCategories"])
