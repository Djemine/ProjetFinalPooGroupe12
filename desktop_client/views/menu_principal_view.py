"""
Fenêtre principale affichée après connexion : une barre de menu (sidebar)
à gauche pour naviguer entre les différentes classes métier (Bus, Trajets,
Passagers, Chauffeurs, Réservations) et une zone de contenu à droite qui
affiche l'écran sélectionné.
"""

import customtkinter as ctk

from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_HOVER, BLANC,
                    GRIS_FOND, GRIS_TEXTE, ROUGE_ERREUR, POLICE_SOUS_TITRE, POLICE_TEXTE)
from desktop_client.views.dashboard_view import DashboardView
from desktop_client.views.bus_view import BusView
from desktop_client.views.trajets_view import TrajetsView
from desktop_client.views.passagers_view import PassagersView
from desktop_client.views.chauffeurs_view import ChauffeursView
from desktop_client.views.reservations_view import ReservationsView


class MenuPrincipalView(ctk.CTkFrame):
    """
    (clé, libellé affiché, classe de la vue).
    """
    SECTIONS = [
        ("dashboard", "Tableau de bord", DashboardView),
        ("bus", "Bus", BusView),
        ("trajets", "Trajets", TrajetsView),
        ("passagers", "Passagers", PassagersView),
        ("chauffeurs", "Chauffeurs", ChauffeursView),
        ("reservations", "Réservations", ReservationsView),
    ]

    def __init__(self, parent, api_client, admin, on_deconnexion):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client
        self.admin = admin
        self.on_deconnexion = on_deconnexion

        self.vue_actuelle = None
        self.boutons_menu = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._construire_barre_haut()
        self._construire_sidebar()

        self.zone_contenu = ctk.CTkFrame(self, fg_color=GRIS_FOND, corner_radius=0)
        self.zone_contenu.grid(row=1, column=1, sticky="nsew")

        self.afficher_section("dashboard")

    def _construire_barre_haut(self):
        # Barre toujours visible en haut de l'écran, quelle que soit la
        # taille de la fenêtre : la déconnexion doit rester accessible
        # même si la sidebar est plus haute que l'écran (zoom Windows, etc.)
        barre = ctk.CTkFrame(self, height=56, corner_radius=0, fg_color=BLANC,
                              border_width=0)
        barre.grid(row=0, column=0, columnspan=2, sticky="ew")
        barre.grid_propagate(False)

        self.label_titre_section = ctk.CTkLabel(
            barre, text="", font=POLICE_SOUS_TITRE, text_color=BLEU_PRINCIPAL)
        self.label_titre_section.pack(side="left", padx=24)

        identifiant = self.admin.get("identifiant", "admin") if isinstance(self.admin, dict) else str(self.admin)
        ctk.CTkLabel(barre, text=f"Connecté : {identifiant}", font=("Segoe UI", 11),
                     text_color=GRIS_TEXTE).pack(side="right", padx=(0, 16))

        ctk.CTkButton(barre, text="Déconnexion", width=130, corner_radius=8,
                      fg_color=ROUGE_ERREUR, hover_color="#B91C1C",
                      font=POLICE_TEXTE,
                      command=self.on_deconnexion).pack(side="right", padx=20, pady=10)

    def _construire_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=BLEU_PRINCIPAL)
        sidebar.grid(row=1, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        for cle, libelle, _ in self.SECTIONS:
            bouton = ctk.CTkButton(
                sidebar, text=libelle, anchor="w", corner_radius=8,
                fg_color="transparent", hover_color=BLEU_HOVER,
                font=POLICE_TEXTE, height=40,
                command=lambda c=cle: self.afficher_section(c),
            )
            bouton.pack(fill="x", padx=14, pady=(16 if cle == self.SECTIONS[0][0] else 3, 3))
            self.boutons_menu[cle] = bouton

    def afficher_section(self, cle: str):
        # Met en surbrillance le bouton actif
        for c, bouton in self.boutons_menu.items():
            bouton.configure(fg_color=BLEU_HOVER if c == cle else "transparent")

        libelles = {c: libelle for c, libelle, _ in self.SECTIONS}
        self.label_titre_section.configure(text=libelles[cle])

        # Détruit l'écran précédent et instancie le nouveau
        if self.vue_actuelle is not None:
            self.vue_actuelle.destroy()

        classe_vue = {c: cls for c, _, cls in self.SECTIONS}[cle]
        self.vue_actuelle = classe_vue(self.zone_contenu, self.api_client)
        self.vue_actuelle.pack(fill="both", expand=True)

        if hasattr(self.vue_actuelle, "rafraichir"):
            self.vue_actuelle.rafraichir()
