from pydantic import BaseModel


class LoginIn(BaseModel):
    identifiant: str
    mot_de_passe: str


class AdministrateurOut(BaseModel):
    identifiant: str
    nom_complet: str