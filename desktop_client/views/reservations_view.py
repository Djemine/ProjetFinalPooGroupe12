"""
Écran de gestion des réservations : création (avec attribution automatique
d'une place et génération du billet), annulation, et consultation du
billet électronique.
"""

from datetime import datetime
from tkinter import filedialog
import customtkinter as ctk

from desktop_client.assets.api_client import ApiError
from desktop_client.assets.combo_recherche import ComboRecherche
from desktop_client.assets.pdf_billet import generer_pdf_billet
from desktop_client.assets.theme import (BLEU_PRINCIPAL, BLEU_HOVER, GRIS_TEXTE, VERT_SUCCES,
                    POLICE_SOUS_TITRE, POLICE_TEXTE, POLICE_TITRE, ROUGE_ERREUR)


class ReservationsView(ctk.CTkFrame):
    def __init__(self, parent, api_client):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client
        self.map_passagers = {}   # texte affiché -> numero_piece_identite
        self.map_trajets = {}     # texte affiché -> trajet_id
        self.dernier_id_reservation = None

        ctk.CTkLabel(self, text="Réservations", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(anchor="w", padx=30, pady=(24, 12))

        formulaire = ctk.CTkFrame(self, corner_radius=12)
        formulaire.pack(fill="x", padx=30, pady=(0, 16))
        ctk.CTkLabel(formulaire, text="Créer une réservation", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(14, 8))

        self.combo_passager = ComboRecherche(formulaire, placeholder_text="Rechercher un passager...",
                                              largeur=260)
        self.combo_passager.grid(row=1, column=0, padx=10, pady=(0, 14))
        self.combo_trajet = ComboRecherche(formulaire, placeholder_text="Rechercher un trajet...",
                                            largeur=320)
        self.combo_trajet.grid(row=1, column=1, padx=10, pady=(0, 14))
        ctk.CTkButton(formulaire, text="Réserver", command=self.creer_reservation,
                      fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
                      width=130).grid(row=1, column=2, padx=10, pady=(0, 14))

        self.label_erreur = ctk.CTkLabel(self, text="", text_color=ROUGE_ERREUR, font=POLICE_TEXTE)
        self.label_erreur.pack(anchor="w", padx=30)

        corps = ctk.CTkFrame(self, fg_color="transparent")
        corps.pack(fill="both", expand=True, padx=30, pady=(8, 20))
        corps.grid_columnconfigure(0, weight=3)
        corps.grid_columnconfigure(1, weight=2)
        corps.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(corps, text="Réservations existantes", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, sticky="w", pady=(0, 4))
        self.zone_liste = ctk.CTkScrollableFrame(corps, fg_color="transparent")
        self.zone_liste.grid(row=1, column=0, sticky="nsew", padx=(0, 16))

        entete_billet = ctk.CTkFrame(corps, fg_color="transparent")
        entete_billet.grid(row=0, column=1, sticky="ew", pady=(0, 4))
        entete_billet.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(entete_billet, text="Billet électronique", font=POLICE_SOUS_TITRE).grid(
            row=0, column=0, sticky="w")
        self.bouton_telecharger = ctk.CTkButton(
            entete_billet, text="Télécharger (PDF)", width=160,
            fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
            command=self.telecharger_billet, state="disabled")
        self.bouton_telecharger.grid(row=0, column=1, sticky="e")

        self.zone_billet = ctk.CTkTextbox(corps, font=("Consolas", 12))
        self.zone_billet.grid(row=1, column=1, sticky="nsew")
        self.zone_billet.configure(state="disabled")

    def creer_reservation(self):
        texte_passager = self.combo_passager.get()
        texte_trajet = self.combo_trajet.get()

        numero_piece = self.map_passagers.get(texte_passager)
        trajet_id = self.map_trajets.get(texte_trajet)

        if numero_piece is None or trajet_id is None:
            self.label_erreur.configure(text="Choisis un passager et un trajet dans les listes")
            return

        try:
            reservation = self.api_client.creer_reservation(numero_piece, trajet_id)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return

        self.label_erreur.configure(text="")
        self.combo_passager.effacer()
        self.combo_trajet.effacer()
        self.rafraichir()
        self.afficher_billet(reservation["id_reservation"])

    def annuler_reservation(self, id_reservation: int):
        try:
            self.api_client.annuler_reservation(id_reservation)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return
        self.label_erreur.configure(text="")
        self.rafraichir()

    def afficher_billet(self, id_reservation: int):
        try:
            billet = self.api_client.obtenir_billet(id_reservation)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return
        self.zone_billet.configure(state="normal")
        self.zone_billet.delete("1.0", "end")
        self.zone_billet.insert("1.0", billet["resume"])
        self.zone_billet.configure(state="disabled")
        self.dernier_id_reservation = id_reservation
        self.bouton_telecharger.configure(state="normal")

    def telecharger_billet(self):
        texte = self.zone_billet.get("1.0", "end").strip()
        if not texte:
            self.label_erreur.configure(text="Aucun billet à télécharger pour le moment")
            return

        nom_defaut = f"billet_reservation_{self.dernier_id_reservation or ''}.pdf"
        chemin = filedialog.asksaveasfilename(
            title="Enregistrer le billet",
            defaultextension=".pdf",
            filetypes=[("Fichier PDF", "*.pdf")],
            initialfile=nom_defaut,
        )
        if not chemin:
            return

        try:
            generer_pdf_billet(chemin, texte)
        except Exception as e:
            self.label_erreur.configure(text=f"Impossible de créer le PDF : {e}")
            return

        self.label_erreur.configure(text="")

    def rafraichir(self):
        self._rafraichir_combos()
        self._rafraichir_liste()

    def _rafraichir_combos(self):
        try:
            passagers = self.api_client.lister_passagers()
            trajets = self.api_client.lister_trajets()
        except Exception:
            return

        self.map_passagers = {
            f"{p['prenom']} {p['nom']} ({p['numero_piece_identite']})": p["numero_piece_identite"]
            for p in passagers
        }
        self.combo_passager.set_valeurs(list(self.map_passagers.keys()))

        self.map_trajets = {}
        for t in trajets:
            date_aff = datetime.fromisoformat(t["date_heure_depart"]).strftime("%d/%m/%Y %H:%M")
            texte = (f"{t['ville_depart']} → {t['ville_arrivee']} - {date_aff} "
                     f"({t['places_disponibles']} places dispo.)")
            self.map_trajets[texte] = t["id"]
        self.combo_trajet.set_valeurs(list(self.map_trajets.keys()))

    def _rafraichir_liste(self):
        for widget in self.zone_liste.winfo_children():
            widget.destroy()

        try:
            reservations = self.api_client.lister_reservations()
        except Exception:
            return

        if not reservations:
            ctk.CTkLabel(self.zone_liste, text="Aucune réservation pour le moment",
                         text_color="gray").pack(anchor="w", pady=10)
            return

        for r in reservations:
            ligne = ctk.CTkFrame(self.zone_liste, corner_radius=8)
            ligne.pack(fill="x", pady=4)

            statut = "Annulée" if r["annulee"] else "Active"
            couleur_statut = ROUGE_ERREUR if r["annulee"] else VERT_SUCCES

            infos = ctk.CTkFrame(ligne, fg_color="transparent")
            infos.pack(side="left", fill="x", expand=True, padx=12, pady=8)
            ctk.CTkLabel(infos, text=f"{r['passager']} — Place {r['numero_place']}",
                         font=POLICE_TEXTE, anchor="w").pack(anchor="w")
            ctk.CTkLabel(infos, text=r["trajet"], font=("Segoe UI", 11),
                         text_color=GRIS_TEXTE, anchor="w").pack(anchor="w")

            ctk.CTkLabel(ligne, text=statut, text_color=couleur_statut,
                         font=POLICE_TEXTE).pack(side="left", padx=10)

            ctk.CTkButton(ligne, text="Billet", width=80,
                          command=lambda i=r["id_reservation"]: self.afficher_billet(i)
                          ).pack(side="left", padx=6, pady=8)

            if not r["annulee"]:
                ctk.CTkButton(ligne, text="Annuler", width=90, fg_color=ROUGE_ERREUR,
                              hover_color="#B91C1C",
                              command=lambda i=r["id_reservation"]: self.annuler_reservation(i)
                              ).pack(side="left", padx=(0, 12), pady=8)