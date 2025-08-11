import os
import tempfile
import webbrowser
from datetime import date
import logging
from pathlib import Path

from PySide6.QtCore import QSize, QPoint
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QMessageBox, QWidget, QPushButton
from sqlalchemy import String
from sqlalchemy.inspection import inspect

import pandas as pd
from PySide6.QtGui import QPixmap, Qt, QImage, QPainter, QRegion, QIcon, QColor

import shutil

from src.utils.pdf_utils import generar_pdf_doble_cara
from src.utils.rutas import get_data_dir, get_icons_path


def setup_logger():
    log_dir = get_data_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "camera_capture.log"

    logger = logging.getLogger("camera_logger")
    logger.setLevel(logging.DEBUG)

    # Evitar añadir múltiples handlers si ya existe
    if not logger.hasHandlers():
        fh = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


logger = setup_logger()

def save_image_from_label(label, path, modo='guardar'):
    if modo == 'guardar':
        pixmap = label.pixmap()
        if pixmap:
            pixmap.save(path)
    elif modo == 'cargar':
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

def save_temporary_file(origen: Path, destino: Path, nombre: str):
    if not origen.exists():
        print(f"[ADVERTENCIA] {nombre} temporal no encontrada.")
        return None

    shutil.copy(origen, destino)
    print(f"[DEBUG] {nombre} guardada: {destino}")

    origen.unlink(missing_ok=True)  # Limpieza
    return str(destino)


def collect_data_form(ui):
    fecha_qt = ui.fechaNacimiento.date()
    if not fecha_qt.isValid():
        raise ValueError("La fecha de nacimiento es inválida o está vacía.")
    fechaNacimiento = date(fecha_qt.year(), fecha_qt.month(), fecha_qt.day())
    print(fechaNacimiento)

    return{


        "Nombre": ui.nombre.text().strip(),
        "Paterno": ui.paterno.text().strip(),
        "Materno": ui.materno.text().strip(),
        "CURP": ui.curp.text().strip(),
        "FechaNacimiento": fechaNacimiento,
        "Calle": ui.calle.text().strip(),
        "Lote": ui.lote.text().strip(),
        "Manzana": ui.manzana.text().strip(),
        "NumExterior": ui.numExt.text().strip(),
        "NumInterior": ui.numInt.text().strip(),
        "CodigoPostal": ui.codigoPostal.text().strip(),
        "Colonia": ui.colonia.text().strip(),
        "Municipio": ui.municipio.text().strip(),
        "Entidad": ui.entidad.text().strip(),
        "SeccionElectoral": ui.seccionElectoral.text().strip(),
        "Genero": ui.genero.currentText(),
        "Celular": ui.celular.text().strip(),
        "Email": ui.email.text().strip()

    }

def sanitize_data(data: dict) -> dict:
    """Limpia un diccionario: quita espacios en strings, convierte None y NaN a cadena vacía, pero preserva fechas."""
    sanitized = {}
    for k, v in data.items():
        if pd.isna(v):  # NaN o None
            sanitized[k] = ""
        elif isinstance(v, str):
            sanitized[k] = v.strip()
        elif isinstance(v, date):
            sanitized[k] = v  # no lo conviertas a string
        else:
            sanitized[k] = str(v).strip()
    return sanitized



def clean_empty_strings(instance):
    """Limpia campos de texto en un modelo SQLAlchemy para evitar None o 'nan'."""
    for attr in inspect(instance).mapper.column_attrs:
        col = attr.columns[0]
        if isinstance(col.type, String):
            value = getattr(instance, attr.key)
            if pd.isna(value) or (isinstance(value, str) and value.strip().lower() == "nan"):
                setattr(instance, attr.key, "")



def get_temp_path(nombre_archivo: str) -> Path:
    temp_dir = Path(tempfile.gettempdir()) / "credenciales_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / nombre_archivo


def clean_temp_images():
    """
    Elimina imágenes temporales de vista previa y exportación.
    """
    temp_dir = Path(tempfile.gettempdir()) / "credenciales_temp"
    for name in ["credencial_frontal.png", "credencial_reverso.png"]:
        file_path = temp_dir / name
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"[INFO] Eliminado: {file_path}")
            except Exception as e:
                print(f"[WARN] No se pudo eliminar {file_path}: {e}")


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

def render_widget_scaled_with_factor(widget: QWidget, gui_size: QSize, final_size: QSize) -> QImage:
    """
    Renderiza un QWidget diseñado en gui_size, escalándolo proporcionalmente
    para que encaje en final_size sin perder proporción ni calidad.
    """
    original_size = widget.size()
    widget.resize(gui_size)
    widget.ensurePolished()

    image = QImage(final_size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.white)

    painter = QPainter(image)

    scale_x = final_size.width() / gui_size.width()
    scale_y = final_size.height() / gui_size.height()

    # Aplica escala proporcional
    painter.scale(scale_x, scale_y)

    widget.render(
        painter,
        QPoint(0, 0),
        QRegion(),
        QWidget.RenderFlag.DrawChildren | QWidget.RenderFlag.DrawWindowBackground
    )
    painter.end()

    widget.resize(original_size)
    return image




def guardar_qimage_temporal(image: QImage, nombre: str) -> str:
    """
    Guarda una imagen QImage como PNG temporal y retorna su ruta.
    """
    ruta = get_temp_path(nombre)
    image.save(str(ruta))
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
            size_gui = QSize(500, 300)  # Tamaño real del widget en QtDesigner (preview)
            size_real = QSize(1011, 638)  # Tamaño real para impresión CR80 a 300 DPI

            front = render_widget_scaled_with_factor(self.front_widget, size_gui, size_real)
            reverse = render_widget_scaled_with_factor(self.back_widget, size_gui, size_real)

            self.front_image = guardar_qimage_temporal(front, "credencial_frontal.png")
            self.reverse_image = guardar_qimage_temporal(reverse, "credencial_reverso.png")

            print(f"[EXPORT] Frontal: {self.front_image}")
            print(f"[EXPORT] Reverso: {self.reverse_image}")

        except Exception as e:
            print(f"[ERROR] Exportación: {e}")
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





