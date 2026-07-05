from datetime import datetime
from pydantic import BaseModel


class ReservationIn(BaseModel):
    numero_piece_identite: str
    trajet_id: int


class ReservationOut(BaseModel):
    id_reservation: int
    passager: str
    trajet: str
    numero_place: int
    date_reservation: datetime
    reference_billet: str
    annulee: bool


class BilletOut(BaseModel):
    reference: str
    resume: str