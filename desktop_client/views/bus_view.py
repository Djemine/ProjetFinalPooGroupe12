"""
Écran de gestion des bus : ajout et consultation de la flotte.
"""

import customtkinter as ctk

from desktop_client.assets.api_client import ApiError
from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_HOVER, GRIS_BORDURE, GRIS_TEXTE,
                    POLICE_SOUS_TITRE, POLICE_TEXTE, POLICE_TITRE, ROUGE_ERREUR)


class BusView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client

        ctk.CTkLabel(self, text="Gestion des bus", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(anchor="w", padx=30, pady=(24, 12))

        formulaire = ctk.CTkFrame(self, corner_radius=12)
        formulaire.pack(fill="x", padx=30, pady=(0, 16))
        ctk.CTkLabel(formulaire, text="Ajouter un bus", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(14, 8))

        self.entree_immat = ctk.CTkEntry(formulaire, placeholder_text="Immatriculation", width=180)
        self.entree_immat.grid(row=1, column=0, padx=10, pady=(0, 14))
        self.entree_marque = ctk.CTkEntry(formulaire, placeholder_text="Marque", width=180)
        self.entree_marque.grid(row=1, column=1, padx=10, pady=(0, 14))
        self.entree_places = ctk.CTkEntry(formulaire, placeholder_text="Nombre de places", width=160)
        self.entree_places.grid(row=1, column=2, padx=10, pady=(0, 14))
        ctk.CTkButton(formulaire, text="Ajouter", command=self.ajouter_bus,
                      fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
                      width=120).grid(row=1, column=3, padx=10, pady=(0, 14))

        self.label_erreur = ctk.CTkLabel(self, text="", text_color=ROUGE_ERREUR, font=POLICE_TEXTE)
        self.label_erreur.pack(anchor="w", padx=30)

        ctk.CTkLabel(self, text="Flotte actuelle", font=POLICE_SOUS_TITRE).pack(
            anchor="w", padx=30, pady=(8, 4))

        entete = ctk.CTkFrame(self, fg_color="transparent")
        entete.pack(fill="x", padx=32)
        for texte, largeur in [("Immatriculation", 200), ("Marque", 220),
                                ("Places totales", 150), ("Places disponibles", 170)]:
            ctk.CTkLabel(entete, text=texte, font=POLICE_SOUS_TITRE, text_color=GRIS_TEXTE,
                         width=largeur, anchor="w").pack(side="left")

        self.zone_liste = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.zone_liste.pack(fill="both", expand=True, padx=30, pady=(4, 20))

    def ajouter_bus(self):
        immat = self.entree_immat.get().strip()
        marque = self.entree_marque.get().strip()
        places = self.entree_places.get().strip()

        if not immat or not marque or not places:
            self.label_erreur.configure(text="Tous les champs sont obligatoires")
            return
        try:
            nombre_places = int(places)
        except ValueError:
            self.label_erreur.configure(text="Le nombre de places doit être un entier")
            return

        try:
            self.api_client.creer_bus(immat, marque, nombre_places)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return

        self.label_erreur.configure(text="")
        self.entree_immat.delete(0, "end")
        self.entree_marque.delete(0, "end")
        self.entree_places.delete(0, "end")
        self.rafraichir()

    def rafraichir(self):
        for widget in self.zone_liste.winfo_children():
            widget.destroy()

        try:
            bus_liste = self.api_client.lister_bus()
        except Exception:
            return

        if not bus_liste:
            ctk.CTkLabel(self.zone_liste, text="Aucun bus enregistré pour le moment",
                         text_color="gray").pack(anchor="w", pady=10)
            return

        for bus in bus_liste:
            ligne = ctk.CTkFrame(self.zone_liste, fg_color="transparent")
            ligne.pack(fill="x", pady=4)
            ctk.CTkLabel(ligne, text=bus["immatriculation"], width=200, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=bus["marque"], width=220, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=str(bus["nombre_places"]), width=150, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=str(bus["places_disponibles"]), width=170, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")