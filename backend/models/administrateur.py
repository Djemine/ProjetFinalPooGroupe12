"""
Classe Administrateur.

Relation illustrée : HERITAGE (Administrateur hérite de Personne)

C'est le SEUL acteur du système : lui seul se connecte à l'application
desktop et gère bus, chauffeurs, trajets, passagers, réservations et
billets. Contrairement à l'ancienne version du projet, il n'y a plus de
classe Compte séparée : l'identifiant et le mot de passe sont directement
portés par l'Administrateur, puisque c'est le seul profil de connexion.
"""

from .personne import Personne


class Administrateur(Personne):
    """Administrateur : gère l'intégralité de la compagnie depuis
    l'application desktop."""

    def __init__(self, nom: str, prenom: str, telephone: str,
                 identifiant: str, mot_de_passe: str):
        super().__init__(nom, prenom, telephone)
        self.identifiant = identifiant
        self.mot_de_passe = mot_de_passe

    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        return self.mot_de_passe == mot_de_passe

    def __str__(self) -> str:
        return f"Administrateur: {self.nom_complet()} ({self.identifiant})"
