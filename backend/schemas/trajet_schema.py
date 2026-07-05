from datetime import datetime
from pydantic import BaseModel, Field


class TrajetIn(BaseModel):
    ville_depart: str
    ville_arrivee: str
    date_heure_depart: datetime
    prix: float = Field(gt=0)
    immatriculation_bus: str


class TrajetOut(BaseModel):
    id: int
    ville_depart: str
    ville_arrivee: str
    date_heure_depart: datetime
    prix: float
    immatriculation_bus: str
    places_disponibles: int