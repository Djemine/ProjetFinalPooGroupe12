"""
Service Reservation : crée les passagers et les réservations (ce qui
déclenche automatiquement la création du Billet, par composition).

Au démarrage, recharge les passagers et reconstruit fidèlement les
réservations déjà enregistrées : chaque place occupée en base est
remarquée comme occupée sur le bon Bus, sans rejouer l'attribution
automatique (qui choisirait une autre place libre).
"""

from datetime import datetime
from models import Passager, Reservation


class ReservationService:
    def __init__(self, db_manager, trajet_service):
        self.db = db_manager
        self.trajet_service = trajet_service
        self.passagers = {}
        self.reservations = []

        self._recharger_passagers()
        self._recharger_reservations()

    def _recharger_passagers(self):
        for ligne in self.db.lister_passagers():
            passager = Passager(ligne["nom"], ligne["prenom"], ligne["telephone"],
                                 ligne["numero_piece_identite"])
            self.passagers[ligne["numero_piece_identite"]] = passager

    def _recharger_reservations(self):
        for ligne in self.db.lister_reservations():
            trajet = self.trajet_service.trouver_trajet(ligne["trajet_id"])
            passager = self.passagers.get(ligne["numero_piece_identite"])
            if trajet is None or passager is None:
                continue

            place = next((p for p in trajet.bus.places
                          if p.numero == ligne["numero_place"]), None)
            if place is None:
                continue

            # Reconstruction sans passer par __init__ (qui choisirait
            # automatiquement une nouvelle place) : on restaure l'état
            # exact qui était enregistré en base.
            reservation = Reservation.__new__(Reservation)
            reservation.id_reservation = ligne["id"]
            reservation.passager = passager
            reservation.trajet = trajet
            reservation.date_reservation = datetime.fromisoformat(ligne["date_reservation"])
            reservation.place = place
            reservation.annulee = bool(ligne["annulee"])

            if not reservation.annulee:
                place.reserver()

            reservation.billet = None  # billet historique non recréé (pas de PDF à ce stade)
            reservation.billet_reference = ligne["reference_billet"]

            passager.ajouter_reservation(reservation)
            self.reservations.append(reservation)

        if self.reservations:
            Reservation._compteur_id = max(r.id_reservation for r in self.reservations) + 1

    def creer_passager(self, nom: str, prenom: str, telephone: str,
                        numero_piece_identite: str) -> Passager:
        if numero_piece_identite in self.passagers:
            raise ValueError("Un passager avec cette pièce d'identité existe déjà.")
        passager = Passager(nom, prenom, telephone, numero_piece_identite)
        self.passagers[numero_piece_identite] = passager
        self.db.ajouter_passager(numero_piece_identite, nom, prenom, telephone)
        return passager

    def creer_reservation(self, numero_piece_identite: str, trajet_id: int) -> Reservation:
        passager = self.passagers.get(numero_piece_identite)
        if passager is None:
            raise ValueError("Passager introuvable.")

        trajet = self.trajet_service.trouver_trajet(trajet_id)
        if trajet is None:
            raise ValueError("Trajet introuvable.")

        reservation = Reservation(passager, trajet)  # crée aussi le Billet (composition)
        reservation.billet_reference = reservation.billet.reference

        self.db.ajouter_reservation(
            numero_piece_identite, trajet.id, reservation.place.numero,
            reservation.date_reservation.isoformat(), reservation.billet.reference)

        self.reservations.append(reservation)
        return reservation

    def annuler_reservation(self, id_reservation: int) -> None:
        reservation = next((r for r in self.reservations
                             if r.id_reservation == id_reservation), None)
        if reservation is None:
            raise ValueError("Réservation introuvable.")
        if reservation.annulee:
            raise ValueError("Cette réservation est déjà annulée.")

        reservation.annuler()
        self.db.annuler_reservation(id_reservation)

    def lister_reservations(self):
        return self.reservations