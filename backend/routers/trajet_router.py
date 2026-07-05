"""
Routes de gestion des trajets.
"""

from typing import List
from fastapi import APIRouter, HTTPException

from .dependencies import trajet_service
from schemas import TrajetIn, TrajetOut

router = APIRouter(prefix="/trajets", tags=["Trajets"])


def _vers_trajet_out(trajet) -> TrajetOut:
    return TrajetOut(
        id=trajet.id,
        ville_depart=trajet.ville_depart,
        ville_arrivee=trajet.ville_arrivee,
        date_heure_depart=trajet.date_heure_depart,
        prix=trajet.prix,
        immatriculation_bus=trajet.bus.immatriculation,
        places_disponibles=trajet.places_disponibles(),
    )


@router.get("", response_model=List[TrajetOut])
def lister_trajets():
    return [_vers_trajet_out(t) for t in trajet_service.lister_trajets()]


@router.post("", response_model=TrajetOut, status_code=201)
def creer_trajet(data: TrajetIn):
    try:
        trajet = trajet_service.creer_trajet(**data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _vers_trajet_out(trajet)


@router.get("/{trajet_id}", response_model=TrajetOut)
def obtenir_trajet(trajet_id: int):
    trajet = trajet_service.trouver_trajet(trajet_id)
    if trajet is None:
        raise HTTPException(status_code=404, detail="Trajet introuvable")
    return _vers_trajet_out(trajet)