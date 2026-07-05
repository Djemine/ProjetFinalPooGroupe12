"""
Classe Passager.

Relation illustrée : HERITAGE (Passager hérite de Personne)

Important : le Passager n'a plus de compte de connexion. Il n'est pas un
acteur du système — c'est une simple fiche de données gérée entièrement
par l'Administrateur (création, historique, réservations pour son compte).
"""

from .personne import Personne


class Passager(Personne):
    """Un passager est une Personne au nom de laquelle des réservations
    sont effectuées par l'administrateur."""

    def __init__(self, nom: str, prenom: str, telephone: str, numero_piece_identite: str):
        super().__init__(nom, prenom, telephone)
        self.numero_piece_identite = numero_piece_identite
        self.historique_reservations = []  # rempli via Reservation (association)

    def ajouter_reservation(self, reservation) -> None:
        self.historique_reservations.append(reservation)

    def __str__(self) -> str:
        return f"Passager: {self.nom_complet()} (CNIB: {self.numero_piece_identite})"
