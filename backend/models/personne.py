"""
Classe mère Personne.

Relation illustrée : HERITAGE
    Passager, Administrateur et Chauffeur héritent tous de Personne.
"""

from abc import ABC


class Personne(ABC):
    """Classe abstraite regroupant les attributs communs à toute personne
    intervenant dans le système (passager, administrateur, chauffeur, ...).
    """

    def __init__(self, nom: str, prenom: str, telephone: str):
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone

    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}"

    def __str__(self) -> str:
        return self.nom_complet()
