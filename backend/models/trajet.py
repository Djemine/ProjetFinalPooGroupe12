"""
Classe Trajet.

Relation illustrée : ASSOCIATION (Trajet <-> Bus, Trajet <-> Reservation)

Simplification pédagogique : les places disponibles sont celles du Bus
associé (composition Bus--Place). On considère donc qu'un bus n'assure
qu'un trajet à la fois — ce qui suffit largement pour la démonstration
des relations POO demandées par le projet.
"""

from datetime import datetime
from .bus import Bus


class Trajet:
    """Représente un trajet proposé par la compagnie
    (ex: Ouagadougou -> Bobo-Dioulasso)."""

    def __init__(self, ville_depart: str, ville_arrivee: str,
                 date_heure_depart: datetime, prix: float, bus: Bus):
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.date_heure_depart = date_heure_depart
        self.prix = prix
        self.bus = bus  # ASSOCIATION : un trajet utilise un bus existant

    def places_disponibles(self) -> int:
        return self.bus.places_disponibles()

    def __str__(self) -> str:
        return (f"{self.ville_depart} -> {self.ville_arrivee} "
                f"le {self.date_heure_depart:%d/%m/%Y %H:%M} ({self.prix} FCFA)")
