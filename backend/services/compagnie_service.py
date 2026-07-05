"""
Service Compagnie : orchestre la création des bus et chauffeurs,
et garde en mémoire les objets métier tout en les persistant en base.

Au démarrage, recharge automatiquement tout ce qui existait déjà
dans la base (flotte de bus, chauffeurs, infos de la compagnie).
"""

from models import Compagnie, Bus, Chauffeur


class CompagnieService:
    def __init__(self, db_manager, nom_compagnie: str, ville_siege: str):
        self.db = db_manager
        self.chauffeurs = []

        # Recharge la compagnie si elle existe déjà en base, sinon la crée
        ligne = self.db.charger_compagnie()
        if ligne is not None:
            self.compagnie = Compagnie(nom=ligne["nom"], ville_siege=ligne["ville_siege"])
        else:
            self.compagnie = Compagnie(nom=nom_compagnie, ville_siege=ville_siege)
            self.db.enregistrer_compagnie(nom_compagnie, ville_siege)

        self._recharger_flotte()
        self._recharger_chauffeurs()

    def _recharger_flotte(self):
        """Reconstruit les objets Bus (et donc leurs Places, par
        composition) à partir de ce qui est déjà en base."""
        for ligne in self.db.lister_bus():
            bus = Bus(ligne["immatriculation"], ligne["marque"], ligne["nombre_places"])
            self.compagnie.flotte.append(bus)

    def _recharger_chauffeurs(self):
        """Reconstruit les objets Chauffeur et réassocie chacun à son bus."""
        for ligne in self.db.lister_chauffeurs():
            chauffeur = Chauffeur(ligne["nom"], ligne["prenom"], ligne["telephone"],
                                   ligne["numero_permis"])
            bus = self.trouver_bus(ligne["immatriculation_bus"])
            if bus is not None:
                chauffeur.assigner_bus(bus)
            self.chauffeurs.append(chauffeur)

    def creer_bus(self, immatriculation: str, marque: str, nombre_places: int) -> Bus:
        if self.trouver_bus(immatriculation) is not None:
            raise ValueError("Un bus avec cette immatriculation existe déjà.")
        bus = Bus(immatriculation, marque, nombre_places)
        self.compagnie.ajouter_bus(bus)
        self.db.ajouter_bus(immatriculation, marque, nombre_places)
        return bus

    def creer_chauffeur(self, nom: str, prenom: str, telephone: str,
                         numero_permis: str, immatriculation_bus: str) -> Chauffeur:
        bus = self.trouver_bus(immatriculation_bus)
        if bus is None:
            raise ValueError("Bus introuvable pour ce chauffeur.")
        chauffeur = Chauffeur(nom, prenom, telephone, numero_permis)
        chauffeur.assigner_bus(bus)
        self.db.ajouter_chauffeur(numero_permis, nom, prenom, telephone, immatriculation_bus)
        self.chauffeurs.append(chauffeur)
        return chauffeur

    def trouver_bus(self, immatriculation: str) -> Bus:
        return next((b for b in self.compagnie.flotte
                     if b.immatriculation == immatriculation), None)

    def lister_bus(self):
        return self.compagnie.flotte

    def lister_chauffeurs(self):
        return self.chauffeurs