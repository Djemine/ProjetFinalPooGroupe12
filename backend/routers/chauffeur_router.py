"""
Routes de gestion des chauffeurs.
"""

from typing import List
from fastapi import APIRouter, HTTPException

from .dependencies import compagnie_service
from schemas import ChauffeurIn, ChauffeurOut

router = APIRouter(prefix="/chauffeurs", tags=["Chauffeurs"])


def _vers_chauffeur_out(chauffeur) -> ChauffeurOut:
    return ChauffeurOut(
        nom=chauffeur.nom,
        prenom=chauffeur.prenom,
        telephone=chauffeur.telephone,
        numero_permis=chauffeur.numero_permis,
        immatriculation_bus=(chauffeur.bus_assigne.immatriculation
                              if chauffeur.bus_assigne else None),
    )


@router.get("", response_model=List[ChauffeurOut])
def lister_chauffeurs():
    return [_vers_chauffeur_out(c) for c in compagnie_service.lister_chauffeurs()]


@router.post("", response_model=ChauffeurOut, status_code=201)
def creer_chauffeur(data: ChauffeurIn):
    try:
        chauffeur = compagnie_service.creer_chauffeur(**data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _vers_chauffeur_out(chauffeur)