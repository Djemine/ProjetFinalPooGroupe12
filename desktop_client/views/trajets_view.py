
"""
Écran de gestion des trajets.
"""

from datetime import datetime
import customtkinter as ctk

from desktop_client.assets.api_client import ApiError
from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_HOVER, GRIS_TEXTE,
                    POLICE_SOUS_TITRE, POLICE_TEXTE, POLICE_TITRE, ROUGE_ERREUR)


class TrajetsView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client

        ctk.CTkLabel(self, text="Gestion des trajets", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(anchor="w", padx=30, pady=(24, 12))

        formulaire = ctk.CTkFrame(self, corner_radius=12)
        formulaire.pack(fill="x", padx=30, pady=(0, 16))
        ctk.CTkLabel(formulaire, text="Ajouter un trajet", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, columnspan=6, sticky="w", padx=16, pady=(14, 8))

        self.e_depart = ctk.CTkEntry(formulaire, placeholder_text="Ville départ", width=140)
        self.e_depart.grid(row=1, column=0, padx=8, pady=(0, 14))
        self.e_arrivee = ctk.CTkEntry(formulaire, placeholder_text="Ville arrivée", width=140)
        self.e_arrivee.grid(row=1, column=1, padx=8, pady=(0, 14))
        self.e_date = ctk.CTkEntry(formulaire, placeholder_text="JJ/MM/AAAA HH:MM", width=150)
        self.e_date.grid(row=1, column=2, padx=8, pady=(0, 14))
        self.e_prix = ctk.CTkEntry(formulaire, placeholder_text="Prix (FCFA)", width=110)
        self.e_prix.grid(row=1, column=3, padx=8, pady=(0, 14))
        self.e_immat = ctk.CTkEntry(formulaire, placeholder_text="Immatriculation bus", width=150)
        self.e_immat.grid(row=1, column=4, padx=8, pady=(0, 14))
        ctk.CTkButton(formulaire, text="Ajouter", command=self.ajouter_trajet,
                      fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
                      width=110).grid(row=1, column=5, padx=8, pady=(0, 14))

        self.label_erreur = ctk.CTkLabel(self, text="", text_color=ROUGE_ERREUR, font=POLICE_TEXTE)
        self.label_erreur.pack(anchor="w", padx=30)

        ctk.CTkLabel(self, text="Trajets proposés", font=POLICE_SOUS_TITRE).pack(
            anchor="w", padx=30, pady=(8, 4))

        entete = ctk.CTkFrame(self, fg_color="transparent")
        entete.pack(fill="x", padx=32)
        for texte, largeur in [("Trajet", 260), ("Date/heure", 160),
                                ("Prix", 110), ("Bus", 140), ("Places dispo.", 120)]:
            ctk.CTkLabel(entete, text=texte, font=POLICE_SOUS_TITRE, text_color=GRIS_TEXTE,
                         width=largeur, anchor="w").pack(side="left")

        self.zone_liste = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.zone_liste.pack(fill="both", expand=True, padx=30, pady=(4, 20))

    def ajouter_trajet(self):
        depart = self.e_depart.get().strip()
        arrivee = self.e_arrivee.get().strip()
        date_texte = self.e_date.get().strip()
        prix = self.e_prix.get().strip()
        immat = self.e_immat.get().strip()

        if not all([depart, arrivee, date_texte, prix, immat]):
            self.label_erreur.configure(text="Tous les champs sont obligatoires")
            return

        try:
            date_dt = datetime.strptime(date_texte, "%d/%m/%Y %H:%M")
        except ValueError:
            self.label_erreur.configure(text="Format de date attendu : JJ/MM/AAAA HH:MM")
            return

        try:
            prix_float = float(prix)
        except ValueError:
            self.label_erreur.configure(text="Le prix doit être un nombre")
            return

        try:
            self.api_client.creer_trajet(depart, arrivee, date_dt.isoformat(), prix_float, immat)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return

        self.label_erreur.configure(text="")
        for champ in (self.e_depart, self.e_arrivee, self.e_date, self.e_prix, self.e_immat):
            champ.delete(0, "end")
        self.rafraichir()

    def rafraichir(self):
        for widget in self.zone_liste.winfo_children():
            widget.destroy()

        try:
            trajets = self.api_client.lister_trajets()
        except Exception:
            return

        if not trajets:
            ctk.CTkLabel(self.zone_liste, text="Aucun trajet enregistré pour le moment",
                         text_color="gray").pack(anchor="w", pady=10)
            return

        for t in trajets:
            ligne = ctk.CTkFrame(self.zone_liste, fg_color="transparent")
            ligne.pack(fill="x", pady=4)
            date_affichee = datetime.fromisoformat(t["date_heure_depart"]).strftime("%d/%m/%Y %H:%M")
            ctk.CTkLabel(ligne, text=f"{t['ville_depart']} → {t['ville_arrivee']}", width=260,
                         anchor="w", font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=date_affichee, width=160, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=f"{t['prix']:,.0f} FCFA".replace(",", " "), width=110,
                         anchor="w", font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=t["immatriculation_bus"], width=140, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")
            ctk.CTkLabel(ligne, text=str(t["places_disponibles"]), width=120, anchor="w",
                         font=POLICE_TEXTE).pack(side="left")