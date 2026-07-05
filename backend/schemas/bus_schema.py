from pydantic import BaseModel, Field


class BusIn(BaseModel):
    immatriculation: str
    marque: str
    nombre_places: int = Field(gt=0)


class BusOut(BaseModel):
    immatriculation: str
    marque: str
    nombre_places: int
    places_disponibles: int