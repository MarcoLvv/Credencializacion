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


# === sizes & utils ============================================================
from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QImage, QPainter, QRegion, Qt
from PySide6.QtWidgets import QWidget

CR80_MM = (85.60, 53.98)  # ancho, alto en mm

def cr80_px(dpi: int = 300) -> QSize:
    """Tamaño CR80 en píxeles para un DPI dado."""
    inch_w = CR80_MM[0] / 25.4
    inch_h = CR80_MM[1] / 25.4
    return QSize(int(round(inch_w * dpi)), int(round(inch_h * dpi)))

def render_widget_to_image(
    widget: QWidget,
    target_size: QSize,
    *,
    scale_from_natural: bool = False,
    bg_color = Qt.GlobalColor.white,
) -> QImage:
    """
    Renderiza un QWidget a QImage del tamaño final deseado.
    - scale_from_natural=False: redimensiona temporalmente el widget a target_size y renderiza (máxima nitidez).
    - scale_from_natural=True: renderiza al tamaño natural del widget y luego escala el QImage (seguro si tu layout no se
      estira con resize()).
    """
    if scale_from_natural:
        natural_size = widget.size()
        image = QImage(natural_size, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(bg_color)
        painter = QPainter(image)
        widget.render(
            painter,
            QPoint(0, 0),
            QRegion(),
            QWidget.RenderFlag.DrawChildren | QWidget.RenderFlag.DrawWindowBackground
        )
        painter.end()
        return image.scaled(
            target_size,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    else:
        original = widget.size()
        widget.resize(target_size)
        widget.ensurePolished()
        if widget.layout():
            widget.layout().activate()
        widget.updateGeometry()
        widget.repaint()

        image = QImage(target_size, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(bg_color)
        painter = QPainter(image)
        widget.render(
            painter,
            QPoint(0, 0),
            QRegion(),
            QWidget.RenderFlag.DrawChildren | QWidget.RenderFlag.DrawWindowBackground
        )
        painter.end()

        widget.resize(original)
        return image

def guardar_qimage_png_temp(image: QImage, ruta: str) -> str:
    image.save(ruta, "PNG", 100)
    return ruta
