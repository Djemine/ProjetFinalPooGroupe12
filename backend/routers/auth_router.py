"""
Routes d'authentification. L'administrateur se connecte depuis
l'application desktop en envoyant identifiant + mot de passe ici.
"""

from fastapi import APIRouter, HTTPException

from .dependencies import auth_service

from schemas import LoginIn, AdministrateurOut

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=AdministrateurOut)
def se_connecter(data: LoginIn):
    admin = auth_service.authentifier(data.identifiant, data.mot_de_passe)
    if admin is None:
        raise HTTPException(status_code=401, detail="Identifiant ou mot de passe incorrect")
    return AdministrateurOut(identifiant=admin.identifiant, nom_complet=admin.nom_complet())