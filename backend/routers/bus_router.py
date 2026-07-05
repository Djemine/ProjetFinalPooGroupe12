"""
Routes de gestion des bus (CRUD partiel : ajout, liste, suppression).
"""

from typing import List
from fastapi import APIRouter, HTTPException

from .dependencies import compagnie_service, db
from schemas import BusIn, BusOut

router = APIRouter(prefix="/bus", tags=["Bus"])


def _vers_bus_out(bus) -> BusOut:
    return BusOut(
        immatriculation=bus.immatriculation,
        marque=bus.marque,
        nombre_places=bus.nombre_places,
        places_disponibles=bus.places_disponibles(),
    )


@router.get("", response_model=List[BusOut])
def lister_bus():
    return [_vers_bus_out(b) for b in compagnie_service.lister_bus()]


@router.post("", response_model=BusOut, status_code=201)
def creer_bus(data: BusIn):
    try:
        bus = compagnie_service.creer_bus(**data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _vers_bus_out(bus)


@router.get("/{immatriculation}", response_model=BusOut)
def obtenir_bus(immatriculation: str):
    bus = compagnie_service.trouver_bus(immatriculation)
    if bus is None:
        raise HTTPException(status_code=404, detail="Bus introuvable")
    return _vers_bus_out(bus)