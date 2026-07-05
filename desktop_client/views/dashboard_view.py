"""
Tableau de bord : vue d'ensemble de l'activité de la compagnie.
"""

import customtkinter as ctk

from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_CLAIR, GRIS_TEXTE, VERT_SUCCES,
                    POLICE_SOUS_TITRE, POLICE_TEXTE, POLICE_TITRE)


class CarteStat(ctk.CTkFrame):
    def __init__(self, parent, titre: str, valeur: str, couleur: str):
        super().__init__(parent, corner_radius=12, fg_color=BLEU_CLAIR, border_width=0)
        ctk.CTkLabel(self, text=titre, font=POLICE_TEXTE, text_color=GRIS_TEXTE).pack(
            anchor="w", padx=18, pady=(16, 0))
        self.label_valeur = ctk.CTkLabel(self, text=valeur, font=("Segoe UI", 26, "bold"),
                                          text_color=couleur)
        self.label_valeur.pack(anchor="w", padx=18, pady=(2, 16))

    def mettre_a_jour(self, valeur: str):
        self.label_valeur.configure(text=valeur)


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client

        ctk.CTkLabel(self, text="Tableau de bord", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(anchor="w", padx=30, pady=(24, 16))

        grille = ctk.CTkFrame(self, fg_color="transparent")
        grille.pack(fill="x", padx=30)
        for i in range(3):
            grille.grid_columnconfigure(i, weight=1, uniform="col")

        self.carte_bus = CarteStat(grille, "Bus en flotte", "0", BLEU_PRINCIPAL)
        self.carte_trajets = CarteStat(grille, "Trajets proposés", "0", BLEU_PRINCIPAL)
        self.carte_passagers = CarteStat(grille, "Passagers enregistrés", "0", BLEU_PRINCIPAL)
        self.carte_reservations = CarteStat(grille, "Réservations actives", "0", VERT_SUCCES)
        self.carte_places = CarteStat(grille, "Places disponibles", "0", VERT_SUCCES)
        self.carte_recettes = CarteStat(grille, "Recettes estimées", "0 FCFA", VERT_SUCCES)

        cartes = [self.carte_bus, self.carte_trajets, self.carte_passagers,
                  self.carte_reservations, self.carte_places, self.carte_recettes]
        for i, carte in enumerate(cartes):
            carte.grid(row=i // 3, column=i % 3, padx=10, pady=10, sticky="nsew")

    def rafraichir(self):
        try:
            stats = self.api_client.statistiques()
        except Exception:
            return
        self.carte_bus.mettre_a_jour(str(stats["nombre_bus"]))
        self.carte_trajets.mettre_a_jour(str(stats["nombre_trajets"]))
        self.carte_passagers.mettre_a_jour(str(stats["nombre_passagers"]))
        self.carte_reservations.mettre_a_jour(str(stats["nombre_reservations"]))
        self.carte_places.mettre_a_jour(str(stats["places_disponibles"]))
        self.carte_recettes.mettre_a_jour(f"{stats['recettes_estimees']:,.0f} FCFA".replace(",", " "))