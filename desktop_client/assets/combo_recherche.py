"""
ComboRecherche : un champ de saisie qui propose une liste filtrée au fur
et à mesure de la frappe
"""

import tkinter as tk
import customtkinter as ctk


class ComboRecherche(ctk.CTkFrame):
    def __init__(self, parent, valeurs=None, placeholder_text="Rechercher...",
                 largeur=280, max_resultats=50, **kwargs_entree):
        super().__init__(parent, fg_color="transparent")
        self.valeurs = valeurs or []
        self.max_resultats = max_resultats
        self.popup = None
        self.liste = None

        self.entree = ctk.CTkEntry(self, placeholder_text=placeholder_text,
                                    width=largeur, **kwargs_entree)
        self.entree.pack()

        self.entree.bind("<KeyRelease>", self._sur_saisie)
        self.entree.bind("<FocusOut>", self._sur_perte_focus)
        self.entree.bind("<Down>", self._aller_vers_liste)
        self.entree.bind("<Escape>", lambda e: self._fermer_popup())

    # --- Interface publique (proche de CTkComboBox) ---
    def set_valeurs(self, valeurs: list):
        self.valeurs = valeurs or []

    def get(self) -> str:
        return self.entree.get()

    def effacer(self):
        self.entree.delete(0, "end")
        self._fermer_popup()

    # --- Filtrage ---
    def _sur_saisie(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"):
            return

        texte = self.entree.get().strip().lower()
        if not texte:
            self._fermer_popup()
            return

        resultats = [v for v in self.valeurs if texte in v.lower()][:self.max_resultats]
        if not resultats:
            self._fermer_popup()
            return
        self._afficher_popup(resultats)

    def _afficher_popup(self, resultats):
        if self.popup is None:
            self.popup = tk.Toplevel(self)
            self.popup.wm_overrideredirect(True)
            self.popup.attributes("-topmost", True)
            self.liste = tk.Listbox(
                self.popup, activestyle="none", relief="flat",
                font=("Segoe UI", 12), highlightthickness=1,
                highlightbackground="#D1D5DB", selectbackground="#1E40AF",
                selectforeground="white",
            )
            self.liste.pack(fill="both", expand=True)
            self.liste.bind("<ButtonRelease-1>", self._sur_selection)
            self.liste.bind("<Return>", self._sur_selection)
            self.liste.bind("<Escape>", lambda e: self._fermer_popup())

        x = self.entree.winfo_rootx()
        y = self.entree.winfo_rooty() + self.entree.winfo_height() + 2
        largeur = max(self.entree.winfo_width(), 200)
        hauteur = min(200, 24 * len(resultats) + 6)
        self.popup.geometry(f"{largeur}x{hauteur}+{x}+{y}")

        self.liste.delete(0, "end")
        for r in resultats:
            self.liste.insert("end", r)
        self.popup.deiconify()

    def _fermer_popup(self):
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None
            self.liste = None

    def _sur_selection(self, event=None):
        if self.liste is None or not self.liste.curselection():
            return
        valeur = self.liste.get(self.liste.curselection()[0])
        self.entree.delete(0, "end")
        self.entree.insert(0, valeur)
        self._fermer_popup()
        self.entree.focus_set()

    def _aller_vers_liste(self, event):
        if self.liste is not None:
            self.liste.focus_set()
            self.liste.selection_set(0)

    def _sur_perte_focus(self, event):
        # Léger délai : si la perte de focus vient d'un clic sur la liste,
        # on laisse cet évènement se traiter avant de fermer le popup.
        self.after(150, self._fermer_si_hors_liste)

    def _fermer_si_hors_liste(self):
        if self.popup is None:
            return
        if self.focus_get() is self.liste:
            return
        self._fermer_popup()
