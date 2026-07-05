"""
Classe Compagnie.

Relation illustrée : AGGREGATION
    Une Compagnie possède une flotte de Bus et une liste de Trajets, mais
    un Bus (ou un Trajet) peut exister indépendamment et être détaché de
    la compagnie sans être détruit. C'est le critère de l'agrégation
    (par opposition à la composition).
"""

from typing import List
from .bus import Bus
from .trajet import Trajet


class Compagnie:
    """Représente une compagnie de transport (ex: TSR, STAF, Rakieta)."""

    def __init__(self, nom: str, ville_siege: str):
        self.nom = nom
        self.ville_siege = ville_siege
        self.flotte: List[Bus] = []       # AGGREGATION : liste de Bus existants
        self.trajets: List[Trajet] = []   # AGGREGATION : liste de Trajets existants

    def ajouter_bus(self, bus: Bus) -> None:
        """Ajoute un bus déjà existant à la flotte (agrégation : le bus
        existait avant d'être rattaché à la compagnie)."""
        self.flotte.append(bus)

    def retirer_bus(self, bus: Bus) -> None:
        if bus in self.flotte:
            self.flotte.remove(bus)

    def ajouter_trajet(self, trajet: Trajet) -> None:
        self.trajets.append(trajet)

    def __str__(self) -> str:
        return f"Compagnie {self.nom} ({len(self.flotte)} bus, {len(self.trajets)} trajets)"
