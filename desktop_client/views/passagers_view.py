"""
Écran de gestion des passagers (fiches créées et gérées par l'administrateur).
"""

import customtkinter as ctk

from desktop_client.assets.api_client import ApiError
from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_HOVER, GRIS_TEXTE,
                    POLICE_SOUS_TITRE, POLICE_TEXTE, POLICE_TITRE, ROUGE_ERREUR)


class PassagersView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client

        ctk.CTkLabel(self, text="Gestion des passagers", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(anchor="w", padx=30, pady=(24, 12))

        formulaire = ctk.CTkFrame(self, corner_radius=12)
        formulaire.pack(fill="x", padx=30, pady=(0, 16))
        ctk.CTkLabel(formulaire, text="Ajouter un passager", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, columnspan=5, sticky="w", padx=16, pady=(14, 8))

        self.e_nom = ctk.CTkEntry(formulaire, placeholder_text="Nom", width=150)
        self.e_nom.grid(row=1, column=0, padx=8, pady=(0, 14))
        self.e_prenom = ctk.CTkEntry(formulaire, placeholder_text="Prénom", width=150)
        self.e_prenom.grid(row=1, column=1, padx=8, pady=(0, 14))
        self.e_tel = ctk.CTkEntry(formulaire, placeholder_text="Téléphone", width=150)
        self.e_tel.grid(row=1, column=2, padx=8, pady=(0, 14))
        self.e_cnib = ctk.CTkEntry(formulaire, placeholder_text="N° pièce d'identité", width=170)
        self.e_cnib.grid(row=1, column=3, padx=8, pady=(0, 14))
        ctk.CTkButton(formulaire, text="Ajouter", command=self.ajouter_passager,
                      fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
                      width=110).grid(row=1, column=4, padx=8, pady=(0, 14))

        self.label_erreur = ctk.CTkLabel(self, text="", text_color=ROUGE_ERREUR, font=POLICE_TEXTE)
        self.label_erreur.pack(anchor="w", padx=30)

        ctk.CTkLabel(self, text="Passagers enregistrés", font=POLICE_SOUS_TITRE).pack(
            anchor="w", padx=30, pady=(8, 4))

        entete = ctk.CTkFrame(self, fg_color="transparent")
        entete.pack(fill="x", padx=32)
        for texte, largeur in [("Nom complet", 220), ("Téléphone", 150),
                                ("N° pièce d'identité", 180), ("Réservations", 130)]:
            ctk.CTkLabel(entete, text=texte, font=POLICE_SOUS_TITRE, text_color=GRIS_TEXTE,
                         width=largeur, anchor="w").pack(side="left")

        self.zone_liste = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.zone_liste.pack(fill="both", expand=True, padx=30, pady=(4, 20))

    def ajouter_passager(self):
        valeurs = {
            "nom": self.e_nom.get().strip(), "prenom": self.e_prenom.get().strip(),
            "telephone": self.e_tel.get().strip(),
            "numero_piece_identite": self.e_cnib.get().strip(),
        }
        if not all(valeurs.values()):
            self.label_erreur.configure(text="Tous les champs sont obligatoires")
            return

        try:
            self.api_client.creer_passager(**valeurs)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return

        self.label_erreur.configure(text="")
        for champ in (self.e_nom, self.e_prenom, self.e_tel, self.e_cnib):
            champ.delete(0, "end")
        self.rafraichir()

    def rafraichir(self):
        for widget in self.zone_liste.winfo_children():
            widget.destroy()

        try:
            passagers = self.api_client.lister_passagers()
        except Exception:
            return

        if not passagers:
            ctk.CTkLabel(self.zone_liste, text="Aucun passager enregistré pour le moment",
                         text_color="gray").pack(anchor="w", pady=10)
            return

        for p in passagers:
            ligne = ctk.CTkFrame(self.zone_liste, fg_color="transparent")
            ligne.pack(fill="x", pady=4)
            ctk.CTkLabel(ligne, text=f"{p['prenom']} {p['nom']}", width=220, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=p["telephone"], width=150, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=p["numero_piece_identite"], width=180, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=str(p["nombre_reservations"]), width=130, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")