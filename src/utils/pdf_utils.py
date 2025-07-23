import os

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from src.utils.rutas import get_temp_credencial_dir


TEMP_DIR = get_temp_credencial_dir()
CR80_SIZE = (85.6 * mm, 53.98 * mm)  # Tamaño tarjeta CR80 en puntos

def generar_pdf_doble_cara(frente_path, reverso_path):
    """Genera PDF de 2 páginas con fondo blanco y contenido completo"""

    os.makedirs(TEMP_DIR, exist_ok=True)
    pdf_path = os.path.join(TEMP_DIR, "credencial_doble_cara.pdf")

    # Aplicar bordes redondeados a ambas imágenes
    frente_path_rounded = frente_path
    reverso_path_rounded = reverso_path

    c = canvas.Canvas(pdf_path, pagesize=CR80_SIZE)

    # Página 1: Frontal
    c.setFillColorRGB(1, 1, 1)  # Fondo blanco
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)
    c.drawImage(frente_path_rounded, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
    c.showPage()

    # Página 2: Reverso
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)
    c.drawImage(reverso_path_rounded, 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1])
    c.showPage()

    c.save()

    #print(f"[OK] PDF generado correctamente en: {pdf_path}")
    return pdf_path