from pydantic import BaseModel


class PassagerIn(BaseModel):
    nom: str
    prenom: str
    telephone: str
    numero_piece_identite: str


class PassagerOut(BaseModel):
    nom: str
    prenom: str
    telephone: str
    numero_piece_identite: str
    nombre_reservations: int