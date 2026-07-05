"""
Classe Chauffeur.

Relation illustrée : HERITAGE (Chauffeur hérite de Personne)
                      ASSOCIATION (Chauffeur <-> Bus : un chauffeur conduit
                      un bus, mais l'un peut exister sans l'autre)
"""

from .personne import Personne


class Chauffeur(Personne):
    """Un chauffeur est une Personne qui conduit un Bus (association)."""

    def __init__(self, nom: str, prenom: str, telephone: str, numero_permis: str):
        super().__init__(nom, prenom, telephone)
        self.numero_permis = numero_permis
        self.bus_assigne = None  # référence vers Bus -> ASSOCIATION

    def assigner_bus(self, bus) -> None:
        """Associe ce chauffeur à un bus. Aucun des deux objets n'est
        créé ou détruit par l'autre : c'est bien une association simple."""
        self.bus_assigne = bus
        bus.chauffeur = self

    def __str__(self) -> str:
        return f"Chauffeur: {self.nom_complet()} (Permis: {self.numero_permis})"
