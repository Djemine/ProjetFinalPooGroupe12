from typing import Optional
from pydantic import BaseModel


class ChauffeurIn(BaseModel):
    nom: str
    prenom: str
    telephone: str
    numero_permis: str
    immatriculation_bus: str


class ChauffeurOut(BaseModel):
    nom: str
    prenom: str
    telephone: str
    numero_permis: str
    immatriculation_bus: Optional[str] = None