"""
Point central d'instanciation des services.

Tous les routers importent leurs services depuis ce module : cela garantit
qu'une seule instance de chaque service (donc une seule connexion base de
données, un seul état en mémoire) est partagée par toute l'API.
"""

from database import DBManager
from services import (
    AuthService,
    CompagnieService,
    TrajetService,
    ReservationService,
    DashboardService,
)

db = DBManager()

auth_service = AuthService(db)
compagnie_service = CompagnieService(db, nom_compagnie="Rakieta", ville_siege="Ouagadougou")
trajet_service = TrajetService(db, compagnie_service)
reservation_service = ReservationService(db, trajet_service)
dashboard_service = DashboardService(compagnie_service, trajet_service, reservation_service)