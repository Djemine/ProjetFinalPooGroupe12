"""
ApiClient : centralise tous les appels HTTP vers le backend FastAPI.
"""

import requests

BASE_URL = "http://127.0.0.1:8000"


class ApiError(Exception):
    """Erreur métier renvoyée par l'API (ex: places indisponibles)."""
    pass


class ApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    # --- Aide interne ---
    def _traiter(self, reponse: requests.Response):
        if reponse.status_code >= 400:
            try:
                detail = reponse.json().get("detail", "Erreur inconnue")
            except ValueError:
                detail = reponse.text
            raise ApiError(detail)
        if reponse.status_code == 204 or not reponse.content:
            return None
        return reponse.json()

    def _get(self, chemin: str):
        return self._traiter(requests.get(f"{self.base_url}{chemin}", timeout=5))

    def _post(self, chemin: str, data: dict):
        return self._traiter(requests.post(f"{self.base_url}{chemin}", json=data, timeout=5))

    # --- Authentification ---
    def login(self, identifiant: str, mot_de_passe: str) -> dict:
        return self._post("/auth/login", {"identifiant": identifiant, "mot_de_passe": mot_de_passe})

    # --- Dashboard ---
    def statistiques(self) -> dict:
        return self._get("/dashboard")

    # --- Bus ---
    def lister_bus(self) -> list:
        return self._get("/bus")

    def creer_bus(self, immatriculation: str, marque: str, nombre_places: int) -> dict:
        return self._post("/bus", {
            "immatriculation": immatriculation, "marque": marque,
            "nombre_places": nombre_places,
        })

    # --- Chauffeurs ---
    def lister_chauffeurs(self) -> list:
        return self._get("/chauffeurs")

    def creer_chauffeur(self, nom: str, prenom: str, telephone: str,
                         numero_permis: str, immatriculation_bus: str) -> dict:
        return self._post("/chauffeurs", {
            "nom": nom, "prenom": prenom, "telephone": telephone,
            "numero_permis": numero_permis, "immatriculation_bus": immatriculation_bus,
        })

    # --- Trajets ---
    def lister_trajets(self) -> list:
        return self._get("/trajets")

    def creer_trajet(self, ville_depart: str, ville_arrivee: str, date_heure_depart: str,
                      prix: float, immatriculation_bus: str) -> dict:
        return self._post("/trajets", {
            "ville_depart": ville_depart, "ville_arrivee": ville_arrivee,
            "date_heure_depart": date_heure_depart, "prix": prix,
            "immatriculation_bus": immatriculation_bus,
        })

    # --- Passagers ---
    def lister_passagers(self) -> list:
        return self._get("/passagers")

    def creer_passager(self, nom: str, prenom: str, telephone: str,
                        numero_piece_identite: str) -> dict:
        return self._post("/passagers", {
            "nom": nom, "prenom": prenom, "telephone": telephone,
            "numero_piece_identite": numero_piece_identite,
        })

    # --- Réservations ---
    def lister_reservations(self) -> list:
        return self._get("/reservations")

    def creer_reservation(self, numero_piece_identite: str, trajet_id: int) -> dict:
        return self._post("/reservations", {
            "numero_piece_identite": numero_piece_identite, "trajet_id": trajet_id,
        })

    def annuler_reservation(self, id_reservation: int) -> dict:
        return self._post(f"/reservations/{id_reservation}/annuler", {})

    def obtenir_billet(self, id_reservation: int) -> dict:
        return self._get(f"/reservations/{id_reservation}/billet")