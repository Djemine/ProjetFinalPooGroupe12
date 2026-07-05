"""
Routes de gestion des passagers (créés et gérés par l'administrateur).
"""

from typing import List
from fastapi import APIRouter, HTTPException

from .dependencies import reservation_service
from schemas import PassagerIn, PassagerOut

router = APIRouter(prefix="/passagers", tags=["Passagers"])


def _vers_passager_out(passager) -> PassagerOut:
    return PassagerOut(
        nom=passager.nom,
        prenom=passager.prenom,
        telephone=passager.telephone,
        numero_piece_identite=passager.numero_piece_identite,
        nombre_reservations=len(passager.historique_reservations),
    )


@router.get("", response_model=List[PassagerOut])
def lister_passagers():
    return [_vers_passager_out(p) for p in reservation_service.passagers.values()]


@router.post("", response_model=PassagerOut, status_code=201)
def creer_passager(data: PassagerIn):
    try:
        passager = reservation_service.creer_passager(**data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _vers_passager_out(passager)