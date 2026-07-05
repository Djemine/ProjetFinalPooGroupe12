"""
Classe Bus.

Relation illustrée : AGGREGATION (Compagnie <-> Bus, voir compagnie.py)
                      ASSOCIATION (Bus <-> Chauffeur, voir chauffeur.py)
                      COMPOSITION (Bus *-- Place, voir place.py)
"""

from typing import List, Optional
from .place import Place


class Bus:
    """Représente un bus physique appartenant à une compagnie.

    À la création du bus, la liste de ses Places est construite
    automatiquement (COMPOSITION) : les places n'existent que parce que
    le bus existe, et sont détruites avec lui.
    """

    def __init__(self, immatriculation: str, marque: str, nombre_places: int):
        self.immatriculation = immatriculation
        self.marque = marque
        self.nombre_places = nombre_places
        self.chauffeur = None  # référence vers Chauffeur -> ASSOCIATION

        # COMPOSITION : le bus crée lui-même ses places à l'instanciation
        self.places: List[Place] = [Place(numero) for numero in range(1, nombre_places + 1)]

    def places_disponibles(self) -> int:
        return sum(1 for place in self.places if place.disponible)

    def prochaine_place_libre(self) -> Optional[Place]:
        for place in self.places:
            if place.disponible:
                return place
        return None

    def __str__(self) -> str:
        return f"Bus {self.immatriculation} ({self.marque}, {self.nombre_places} places)"
