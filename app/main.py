from fastapi import FastAPI
from app.routers import (
    clinics, professions, users, service_categories, services, patients, patient_lab_results,
    patients_lab_results_details
)

app = FastAPI(title="Mock DobrynyaNN API")

app.include_router(clinics.router, tags=["Clinics"])
app.include_router(professions.router, tags=["Professions"])
app.include_router(users.router, tags=["Users"])
app.include_router(service_categories.router, tags=["ServiceCategories"])
app.include_router(services.router, tags=["Services"])
app.include_router(patients.router, tags=["Patients"])
app.include_router(patient_lab_results.router, tags=["Patient Lab Results"])
app.include_router(patients_lab_results_details.router, tags=["Patient Lab Results Details"])