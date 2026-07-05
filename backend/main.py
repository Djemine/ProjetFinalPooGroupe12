"""
API REST du logiciel de réservation de bus (FastAPI).

Lancer depuis le dossier backend/ avec :
    uvicorn main:app --reload

Puis ouvrir http://127.0.0.1:8000/docs pour la documentation Swagger
générée automatiquement.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    auth_router,
    bus_router,
    chauffeur_router,
    trajet_router,
    passager_router,
    reservation_router,
    dashboard_router,
)

app = FastAPI(
    title="API Réservation de Bus",
    description="Gestion des bus, trajets, passagers et réservations "
                "pour une compagnie de transport au Burkina Faso.",
    version="1.0.0",
)

# Autorise l'application desktop (client HTTP local) à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(bus_router.router)
app.include_router(chauffeur_router.router)
app.include_router(trajet_router.router)
app.include_router(passager_router.router)
app.include_router(reservation_router.router)
app.include_router(dashboard_router.router)


@app.get("/", tags=["Accueil"])
def accueil():
    return {"message": "API de réservation de bus opérationnelle. Voir /docs."}