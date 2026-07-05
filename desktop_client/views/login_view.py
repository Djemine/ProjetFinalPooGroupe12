"""
Écran de connexion. Seul l'Administrateur peut se connecter à
l'application — c'est le seul acteur du système.
"""

import customtkinter as ctk

from desktop_client.assets.api_client import ApiError
from desktop_client.assets.theme import BLEU_PRINCIPAL, BLEU_HOVER, GRIS_TEXTE, POLICE_TITRE, POLICE_TEXTE, ROUGE_ERREUR


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, api_client, on_login_success):
        super().__init__(parent, fg_color="transparent")
        self.api_client = api_client
        self.on_login_success = on_login_success

        conteneur = ctk.CTkFrame(self, width=380, corner_radius=16, border_width=1)
        conteneur.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(conteneur, text="Rakieta Transport", font=POLICE_TITRE,
                     text_color=BLEU_PRINCIPAL).pack(pady=(36, 4), padx=60)
        ctk.CTkLabel(conteneur, text="Espace administrateur", font=POLICE_TEXTE,
                     text_color=GRIS_TEXTE).pack(pady=(0, 24))

        self.entree_identifiant = ctk.CTkEntry(conteneur, placeholder_text="Identifiant",
                                                width=280, height=40)
        self.entree_identifiant.pack(pady=8, padx=40)

        self.entree_mdp = ctk.CTkEntry(conteneur, placeholder_text="Mot de passe",
                                        show="*", width=280, height=40)
        self.entree_mdp.pack(pady=8, padx=40)
        self.entree_mdp.bind("<Return>", lambda e: self.se_connecter())

        self.label_erreur = ctk.CTkLabel(conteneur, text="", text_color=ROUGE_ERREUR,
                                          font=POLICE_TEXTE)
        self.label_erreur.pack(pady=(4, 0))

        ctk.CTkButton(conteneur, text="Se connecter", command=self.se_connecter,
                      fg_color=BLEU_PRINCIPAL, hover_color=BLEU_HOVER,
                      width=280, height=42, corner_radius=8,
                      font=POLICE_TEXTE).pack(pady=(16, 12))

        ctk.CTkLabel(conteneur, text="Compte par défaut : admin / admin123",
                     font=("Segoe UI", 10), text_color="gray").pack(pady=(0, 32))

    def se_connecter(self):
        identifiant = self.entree_identifiant.get().strip()
        mot_de_passe = self.entree_mdp.get().strip()

        if not identifiant or not mot_de_passe:
            self.label_erreur.configure(text="Merci de remplir les deux champs")
            return

        try:
            admin = self.api_client.login(identifiant, mot_de_passe)
        except ApiError as e:
            self.label_erreur.configure(text=str(e))
            return
        except Exception:
            self.label_erreur.configure(
                text="Impossible de joindre l'API. Est-elle bien lancée ?")
            return

        self.label_erreur.configure(text="")
        self.on_login_success(admin)