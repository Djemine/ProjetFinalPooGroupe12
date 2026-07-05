"""
Service Authentification : gère le compte de l'Administrateur, seul
acteur du système. Recharge les administrateurs existants au démarrage
et crée un compte par défaut si aucun n'existe encore.
"""

from models import Administrateur


class AuthService:
    def __init__(self, db_manager):
        self.db = db_manager
        self.administrateurs = {}

        self._recharger_administrateurs()

        if not self.administrateurs:
            self.creer_administrateur(
                nom="Système", prenom="Administrateur", telephone="70000000",
                identifiant="admin", mot_de_passe="admin123")

    def _recharger_administrateurs(self):
        for ligne in self.db.lister_administrateurs():
            admin = Administrateur(
                ligne["nom"], ligne["prenom"], ligne["telephone"],
                ligne["identifiant"], ligne["mot_de_passe"])
            self.administrateurs[ligne["identifiant"]] = admin

    def creer_administrateur(self, nom: str, prenom: str, telephone: str,
                              identifiant: str, mot_de_passe: str) -> Administrateur:
        if identifiant in self.administrateurs:
            raise ValueError("Cet identifiant existe déjà.")
        admin = Administrateur(nom, prenom, telephone, identifiant, mot_de_passe)
        self.administrateurs[identifiant] = admin
        self.db.ajouter_administrateur(identifiant, mot_de_passe, nom, prenom, telephone)
        return admin

    def authentifier(self, identifiant: str, mot_de_passe: str) -> Administrateur:
        admin = self.administrateurs.get(identifiant)
        if admin and admin.verifier_mot_de_passe(mot_de_passe):
            return admin
        return None