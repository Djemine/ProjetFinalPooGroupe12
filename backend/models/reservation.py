"""
Classe Reservation.

Relation illustrée : ASSOCIATION (Reservation <-> Passager, Reservation <-> Trajet,
                      Reservation <-> Place)
                      COMPOSITION (Reservation -> Billet)
"""

from datetime import datetime
from .passager import Passager
from .trajet import Trajet
from .billet import Billet


class Reservation:
    """Représente la réservation d'une place par un passager sur un trajet.

    Créée uniquement par l'Administrateur (le passager n'a pas d'accès
    direct à l'application).
    """

    _compteur_id = 1

    def __init__(self, passager: Passager, trajet: Trajet):
        self.id_reservation = Reservation._compteur_id
        Reservation._compteur_id += 1

        self.passager = passager  # ASSOCIATION
        self.trajet = trajet      # ASSOCIATION
        self.date_reservation = datetime.now()

        place = trajet.bus.prochaine_place_libre()
        if place is None:
            raise ValueError("Plus de places disponibles sur ce trajet.")

        place.reserver()
        self.place = place  # ASSOCIATION : la place concrète attribuée
        self.annulee = False

        passager.ajouter_reservation(self)

        # COMPOSITION : le billet est créé PAR la réservation et n'a pas de
        # sens sans elle. Si la réservation est supprimée, le billet l'est aussi.
        self.billet = Billet(self)

    def annuler(self) -> None:
        self.place.liberer()
        self.annulee = True

    def __str__(self) -> str:
        return (f"Reservation #{self.id_reservation} - {self.passager.nom_complet()} "
                f"sur {self.trajet} - Place {self.place.numero}")