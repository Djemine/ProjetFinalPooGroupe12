"""
Classe Place.

Relation illustrée : COMPOSITION (Bus *-- Place, voir bus.py)

Une Place n'a aucun sens en dehors du Bus qui la contient : elle est créée
en même temps que le bus (dans Bus.__init__) et n'est jamais partagée
entre plusieurs bus. Si le bus est supprimé, ses places disparaissent
avec lui — c'est le critère de la composition (cycle de vie partagé).
"""


class Place:
    """Représente un siège physique à l'intérieur d'un bus."""

    def __init__(self, numero: int):
        self.numero = numero
        self.disponible = True

    def reserver(self) -> None:
        self.disponible = False

    def liberer(self) -> None:
        self.disponible = True

    def __str__(self) -> str:
        etat = "libre" if self.disponible else "occupée"
        return f"Place {self.numero} ({etat})"
