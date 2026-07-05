"""
Classe Billet.

Relation illustrée : COMPOSITION
    Un Billet n'existe que parce qu'une Reservation l'a créé. Il n'a pas
    de cycle de vie propre : sa durée de vie est entièrement liée à celle
    de la Reservation qui l'a produit.
"""

import uuid
from datetime import datetime


class Billet:
    """Billet électronique généré automatiquement lors d'une réservation."""

    def __init__(self, reservation):
        self.reference = str(uuid.uuid4())[:8].upper()
        self.date_emission = datetime.now()
        self.reservation = reservation  # COMPOSITION : lien vers le "tout"

    def resume(self) -> str:
        r = self.reservation
        return (
            f"--- BILLET ELECTRONIQUE ---\n"
            f"Référence : {self.reference}\n"
            f"Passager  : {r.passager.nom_complet()}\n"
            f"Trajet    : {r.trajet}\n"
            f"Bus       : {r.trajet.bus}\n"
            f"Place     : {r.place.numero}\n"
            f"Émis le   : {self.date_emission:%d/%m/%Y %H:%M}\n"
        )

    def generer_pdf(self, chemin: str) -> None:
        """Génère une version PDF imprimable du billet."""
        from fpdf import FPDF

        r = self.reservation
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "BILLET ELECTRONIQUE", ln=True, align="C")
        pdf.set_draw_color(0, 0, 0)
        pdf.line(10, 24, 200, 24)
        pdf.ln(10)

        pdf.set_font("Helvetica", "", 12)
        lignes = [
            ("Reference", self.reference),
            ("Passager", r.passager.nom_complet()),
            ("Trajet", f"{r.trajet.ville_depart} -> {r.trajet.ville_arrivee}"),
            ("Date/Heure", f"{r.trajet.date_heure_depart:%d/%m/%Y %H:%M}"),
            ("Bus", f"{r.trajet.bus.marque} ({r.trajet.bus.immatriculation})"),
            ("Place", str(r.place.numero)),
            ("Prix", f"{r.trajet.prix} FCFA"),
            ("Emis le", f"{self.date_emission:%d/%m/%Y %H:%M}"),
        ]
        for label, valeur in lignes:
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(45, 10, f"{label} :")
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(0, 10, str(valeur), ln=True)

        pdf.output(chemin)

    def __str__(self) -> str:
        return f"Billet {self.reference}"
