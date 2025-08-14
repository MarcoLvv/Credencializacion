import logging
import shutil
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd
from PySide6.QtGui import QPixmap
from sqlalchemy import String
from sqlalchemy.inspection import inspect

from src.utils.rutas import get_data_dir, get_temp_dir


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


def clean_empty_strings(obj):
    """
    Reemplaza atributos de tipo string que sean None o NaN por ""
    Solo aplica a columnas de tipo string declaradas en SQLAlchemy.
    """
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        if isinstance(value, str) and (value is None or str(value).lower() == "nan"):
            setattr(obj, column.name, "")





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

    temp_dir_images = get_temp_dir()  # ruta donde guardas temporales
    if not Path(temp_dir).exists():
        logging.debug(f"No existe carpeta temporal: {temp_dir}")
        return

    for file in Path(temp_dir_images).iterdir():
        try:
            if file.is_file():
                file.unlink()
                logging.debug(f"Archivo temporal eliminado: {file}")
        except Exception as e:
            logging.error(f"No se pudo eliminar {file}: {e}")

