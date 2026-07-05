"""
Service Trajet : crée des trajets liés à un bus existant, les persiste,
et recharge ceux qui existaient déjà en base au démarrage.
"""

from datetime import datetime
from models import Trajet


class TrajetService:
    def __init__(self, db_manager, compagnie_service):
        self.db = db_manager
        self.compagnie_service = compagnie_service
        self.trajets = []
        self._recharger_trajets()

    def _recharger_trajets(self):
        for ligne in self.db.lister_trajets():
            bus = self.compagnie_service.trouver_bus(ligne["immatriculation_bus"])
            if bus is None:
                continue
            date_dep = datetime.fromisoformat(ligne["date_heure_depart"])
            trajet = Trajet(ligne["ville_depart"], ligne["ville_arrivee"],
                             date_dep, ligne["prix"], bus)
            trajet.id = ligne["id"]
            self.trajets.append(trajet)

    def creer_trajet(self, ville_depart: str, ville_arrivee: str,
                      date_heure_depart: datetime, prix: float,
                      immatriculation_bus: str) -> Trajet:
        bus = self.compagnie_service.trouver_bus(immatriculation_bus)
        if bus is None:
            raise ValueError("Bus introuvable pour ce trajet.")

        trajet = Trajet(ville_depart, ville_arrivee, date_heure_depart, prix, bus)
        trajet_id = self.db.ajouter_trajet(
            ville_depart, ville_arrivee, date_heure_depart.isoformat(),
            prix, immatriculation_bus)
        trajet.id = trajet_id
        self.trajets.append(trajet)
        return trajet

    def lister_trajets(self):
        return self.trajets

    def trouver_trajet(self, trajet_id: int) -> Trajet:
        return next((t for t in self.trajets if t.id == trajet_id), None)