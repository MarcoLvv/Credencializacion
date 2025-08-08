import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from PIL import Image

from src.utils.rutas import get_temp_credencial_dir, get_temp_pdf_path

TEMP_DIR = get_temp_credencial_dir()
CR80_SIZE = (85.6 * mm, 53.98 * mm)  # Tamaño tarjeta CR80 en puntos (≈ 242.65 x 153.08 pt)

def verificar_resolucion(imagen_path):
    """Verifica y lanza advertencia si la imagen es menor al tamaño ideal para 300 DPI"""
    with Image.open(str(imagen_path)) as img:
        w, h = img.size
        if w < 1011 or h < 638:
            print(f"[ADVERTENCIA] Imagen {imagen_path} tiene resolución baja: {w}x{h}px (se recomienda 1011x638 para 300 DPI)")

def generar_pdf_doble_cara(frente_path, reverso_path):
    """Genera PDF de 2 páginas con fondo blanco y calidad alta"""

    pdf_path = get_temp_pdf_path()

    verificar_resolucion(str(frente_path))
    verificar_resolucion(str(reverso_path))

    c = canvas.Canvas(pdf_path, pagesize=CR80_SIZE)

    # Página 1: Frente
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)

    c.drawImage(ImageReader(frente_path), 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1], preserveAspectRatio=False, mask='auto')
    c.showPage()

    # Página 2: Reverso
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, CR80_SIZE[0], CR80_SIZE[1], stroke=0, fill=1)
    c.drawImage(ImageReader(reverso_path), 0, 0, width=CR80_SIZE[0], height=CR80_SIZE[1], preserveAspectRatio=False, mask='auto')
    c.showPage()

    c.save()
    return pdf_path