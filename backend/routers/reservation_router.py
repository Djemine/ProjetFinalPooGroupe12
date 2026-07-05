"""
Routes de gestion des réservations et de génération du billet.
"""

from typing import List
from fastapi import APIRouter, HTTPException

from .dependencies import reservation_service
from schemas import ReservationIn, ReservationOut, BilletOut

router = APIRouter(prefix="/reservations", tags=["Reservations"])


def _vers_reservation_out(reservation) -> ReservationOut:
    return ReservationOut(
        id_reservation=reservation.id_reservation,
        passager=reservation.passager.nom_complet(),
        trajet=str(reservation.trajet),
        numero_place=reservation.place.numero,
        date_reservation=reservation.date_reservation,
        reference_billet=reservation.billet_reference,
        annulee=reservation.annulee,
    )


def _resume_billet(reservation) -> str:
    """Reconstruit le résumé du billet même pour une réservation
    rechargée depuis la base (dont l'objet Billet n'est pas recréé)."""
    if reservation.billet is not None:
        return reservation.billet.resume()

    r = reservation
    return (
        f"--- BILLET ELECTRONIQUE ---\n"
        f"Référence : {r.billet_reference}\n"
        f"Passager  : {r.passager.nom_complet()}\n"
        f"Trajet    : {r.trajet}\n"
        f"Bus       : {r.trajet.bus}\n"
        f"Place     : {r.place.numero}\n"
        f"Réservé le : {r.date_reservation:%d/%m/%Y %H:%M}\n"
    )


@router.get("", response_model=List[ReservationOut])
def lister_reservations():
    return [_vers_reservation_out(r) for r in reservation_service.lister_reservations()]


@router.post("", response_model=ReservationOut, status_code=201)
def creer_reservation(data: ReservationIn):
    try:
        reservation = reservation_service.creer_reservation(
            data.numero_piece_identite, data.trajet_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _vers_reservation_out(reservation)


@router.post("/{id_reservation}/annuler", response_model=ReservationOut)
def annuler_reservation(id_reservation: int):
    try:
        reservation_service.annuler_reservation(id_reservation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    reservation = next(r for r in reservation_service.lister_reservations()
                        if r.id_reservation == id_reservation)
    return _vers_reservation_out(reservation)


@router.get("/{id_reservation}/billet", response_model=BilletOut)
def obtenir_billet(id_reservation: int):
    reservation = next((r for r in reservation_service.lister_reservations()
                         if r.id_reservation == id_reservation), None)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Réservation introuvable")
    return BilletOut(reference=reservation.billet_reference, resume=_resume_billet(reservation))