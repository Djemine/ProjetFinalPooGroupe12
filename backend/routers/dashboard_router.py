"""
Route du tableau de bord : statistiques agrégées pour l'écran d'accueil
de l'application desktop.
"""

from fastapi import APIRouter

from .dependencies import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def obtenir_statistiques():
    return dashboard_service.statistiques()