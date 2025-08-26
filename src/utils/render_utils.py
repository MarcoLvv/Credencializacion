import logging
import os
import tempfile
import webbrowser
from pathlib import Path

from PySide6.QtCore import QSize, QPoint
from PySide6.QtGui import QPainter, QRegion, QImage, Qt, QPixmap
from PySide6.QtWidgets import QMessageBox, QWidget, QApplication

from src.utils.helpers import clean_temp_images
from src.utils.pdf_utils import generar_pdf_doble_cara
from src.utils.rutas import get_background_front_side, get_background_back_side


def get_temp_path(nombre_archivo: str) -> Path:
    temp_dir = Path(tempfile.gettempdir()) / "credenciales_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / nombre_archivo




def render_widget_to_qimage(widget: QWidget, target_size: QSize) -> QImage:
    """
    Renderiza un QWidget a un QImage con el tamaño deseado,
    asegurando que el contenido se expanda completamente.
    """


    # Guardar tamaño original
    original_size = widget.size()

    # Redimensionar temporalmente
    widget.resize(target_size)
    widget.ensurePolished()

    # Forzar layout si existe
    layout = widget.layout()
    if layout:
        layout.activate()

    widget.updateGeometry()
    widget.repaint()

    # Crear imagen base
    image = QImage(target_size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.white)

    # Pintar el widget completo
    painter = QPainter(image)
    widget.render(
        painter,
        QPoint(0, 0),
        QRegion(),
        QWidget.RenderFlag.DrawChildren | QWidget.RenderFlag.DrawWindowBackground
    )
    painter.end()

    # Restaurar tamaño original
    widget.resize(original_size)

    return image

def render_widget_scaled(widget: QWidget, final_size: QSize) -> QImage:
    """
    Renderiza el widget directamente a alta resolución usando escalado por QTransform,
    evitando pérdida de nitidez en textos y vectores.
    """
    original_size = widget.size()

    # Crear imagen de salida en resolución final
    image = QImage(final_size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.white)

    # Escala de pintura
    scale_x = final_size.width() / original_size.width()
    scale_y = final_size.height() / original_size.height()

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

    # Escalar el sistema de coordenadas
    painter.scale(scale_x, scale_y)

    # Renderizar el widget con coordenadas escaladas
    widget.render(
        painter,
        QPoint(0, 0),
        QRegion(),
        QWidget.RenderFlag.DrawChildren | QWidget.RenderFlag.DrawWindowBackground
    )

    painter.end()
    return image

def guardar_qimage_temporal(image: QImage, nombre: str) -> str:
    """
    Guarda una imagen QImage como PNG temporal y retorna su ruta.
    """
    ruta = get_temp_path(nombre)
    image.save(str(ruta), "PNG",  -1)
    return str(ruta)


def show_scaled_preview(image_path: str, label_widget, scaled= False):
    """
    Muestra la imagen escalada proporcionalmente dentro del QLabel.
    """
    if Path(image_path).exists():
        pixmap = QPixmap(image_path)
        label_widget.setScaledContents(scaled)

        scaled = pixmap.scaled(
            label_widget.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label_widget.setPixmap(scaled)


class CredencialRenderer:
    """
    Clase que encapsula el proceso de generación de imágenes de credenciales.
    """

    def __init__(self, front_widget: QWidget, back_widget: QWidget, parent=None, db = None):
        self.front_widget = front_widget
        self.back_widget = back_widget
        self.parent = parent  # Para QMessageBox
        self.db = db
        self.front_image = None
        self.reverse_image = None

    def generate_images_for_preview(self):
        """
        Genera imágenes en baja resolución (vista previa).
        """
        try:
            size_preview = QSize(500, 300)

            front = render_widget_to_qimage(self.front_widget, size_preview)
            reverse = render_widget_to_qimage(self.back_widget, size_preview)

            self.front_image = guardar_qimage_temporal(front, "credencial_frontal.png")
            self.reverse_image = guardar_qimage_temporal(reverse, "credencial_reverso.png")

            print(f"[PREVIEW] Frontal: {self.front_image}")
            print(f"[PREVIEW] Reverso: {self.reverse_image}")

        except Exception as e:
            print(f"[ERROR] Vista previa: {e}")
            if self.parent:
                QMessageBox.critical(self.parent.captureView, "Error", f"No se pudo generar la vista previa:\n{e}")

    def generate_images_for_export(self):
        try:
            clean_temp_images()
            size_real = QSize(1011, 638)

            front_label = self.parent.labelFrontBackgroundCredential
            back_label = self.parent.labelReverseBackgroundCredential
            pixmap_front_original = front_label.pixmap()
            pixmap_back_original = back_label.pixmap()

            # 🔹 Detectar qué fondo trasero está puesto

            # Front siempre igual (si tienes variantes también habría que detectarlas)
            front_hd = QPixmap(str(get_background_front_side("front_side")))

            # Back depende de lo que esté actualmente
            if self.parent.checkBoxBackgroundSignature.isChecked():
                back_hd = QPixmap(str(get_background_back_side("back_side")))
            else:
                back_hd = QPixmap(str(get_background_back_side("back_side_wo_signature")))

            # Reemplazar temporalmente
            front_label.setPixmap(front_hd)
            back_label.setPixmap(back_hd)

            # Render en alta resolución
            front = render_widget_scaled(self.front_widget, size_real)
            reverse = render_widget_scaled(self.back_widget, size_real)

            self.front_image = guardar_qimage_temporal(front, "credencial_frontal.png")
            self.reverse_image = guardar_qimage_temporal(reverse, "credencial_reverso.png")

            # Restaurar originales
            front_label.setPixmap(pixmap_front_original)
            back_label.setPixmap(pixmap_back_original)

        except Exception as e:
            logging.error(f"[ERROR] Exportación: {e}")
            if self.parent:
                QMessageBox.critical(self.parent.captureView, "Error", f"No se pudo exportar la credencial:\n{e}")

    def show_pdf_in_browser(self, db):
        """
        Genera el PDF, lo abre en el navegador y actualiza VecesImpresa.
        """
        if not getattr(self, "folio_id", None):
            print("[ERROR] No se ha establecido folio_id para la impresión")
            return

        self.db = db
        self.generate_images_for_export()
        pdf_path = generar_pdf_doble_cara(self.front_image, self.reverse_image)

        if pdf_path and os.path.exists(pdf_path):
            webbrowser.open(pdf_path)

            try:
                self.db.incrementar_veces_impresa(self.folio_id)
                print(f"[DEBUG] VecesImpresa incrementado para folio {self.folio_id}")
                if hasattr(self.parent, "reload_table"):
                    self.parent.reload_table()
            except Exception as e:
                print(f"Error al actualizar VecesImpresa: {e}")
        else:
            if self.parent:
                QMessageBox.warning(self.parent, "PDF", "No se pudo generar el PDF.")


