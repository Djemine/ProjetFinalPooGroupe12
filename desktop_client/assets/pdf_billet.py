"""
Génère le billet électronique au format PDF à partir du résumé texte
renvoyé par l'API (endpoint GET /reservations/{id}/billet).
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

BLEU_PRINCIPAL = "#1E40AF"
GRIS_TEXTE = "#374151"


def generer_pdf_billet(chemin: str, texte_resume: str):
    """Écrit un PDF présentable à `chemin` à partir du texte du billet."""
    doc = SimpleDocTemplate(
        chemin, pagesize=A4,
        topMargin=25 * mm, bottomMargin=25 * mm,
        leftMargin=25 * mm, rightMargin=25 * mm,
    )
    styles = getSampleStyleSheet()

    style_titre = ParagraphStyle(
        "TitreBillet", parent=styles["Title"], textColor=colors.HexColor(BLEU_PRINCIPAL))
    style_soustitre = ParagraphStyle(
        "SousTitreBillet", parent=styles["Normal"], textColor=colors.HexColor(GRIS_TEXTE),
        fontSize=11, spaceAfter=16)
    style_corps = ParagraphStyle(
        "CorpsBillet", parent=styles["Normal"], fontSize=12, leading=19)

    elements = [
        Paragraph("Rakieta Transport", style_titre),
        Paragraph("Billet électronique", style_soustitre),
        HRFlowable(width="100%", color=colors.HexColor(BLEU_PRINCIPAL), thickness=1),
        Spacer(1, 16),
    ]

    for ligne in texte_resume.splitlines():
        ligne = ligne.strip()
        if ligne:
            elements.append(Paragraph(ligne, style_corps))
        else:
            elements.append(Spacer(1, 8))

    doc.build(elements)
