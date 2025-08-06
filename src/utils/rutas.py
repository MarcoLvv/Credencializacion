import sys
from pathlib import Path
from tempfile import gettempdir


def get_base_dir():
    """Devuelve la carpeta base (modo ejecutable o desarrollo)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path.cwd()


def get_data_dir():
    """Crea y devuelve la carpeta /data base del sistema."""
    data_dir = get_base_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_exportaciones_dir():
    """Crea y devuelve la carpeta /data/exportaciones"""
    path = get_data_dir() / "exportaciones"
    path.mkdir(parents=True, exist_ok=True)
    return path

# === Carpetas por tipo ===
def get_styles():
    return get_data_dir() /"resources" / "styles" / "styles.qss"

def get_data_db_dir():
    path = get_data_dir() / "bases"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_excel_dir():
    path = get_data_dir() / "excel"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_static_dir():
    path = get_data_dir() / "static"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_icons_dir():
    path = get_data_dir() / "icons"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_foto_dir():
    path = get_data_dir() / "fotos"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_firma_dir():
    path = get_data_dir() / "firmas"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_dir():
    path = get_data_dir() / "temp"
    path.mkdir(parents=True, exist_ok=True)
    return path

# === Archivos temporales individuales ===

def get_temp_path(nombre_archivo: str):
    """Devuelve la ruta para un archivo temporal dentro de /temp"""
    return get_temp_dir() / nombre_archivo

def get_temp_pdf_path():
    return str(get_temp_path("temp_pdf.pdf"))

def get_temp_foto_path():
    return get_temp_path("temp_foto.png")

def get_temp_firma_path():
    return get_temp_path("temp_firma.png")

# === Rutas de imagenes por folio ===

def get_foto_path(folio_id: str):
    return get_foto_dir() / f"{folio_id}.png"

def get_firma_path(folio_id: str):
    return get_firma_dir() / f"{folio_id}.png"

# === Archivos temporales del PDF de credencial ===

def get_temp_credencial_dir():
    path = Path(gettempdir()) / "credenciales_temp"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_credencial_sides_paths():
    dir_ = get_temp_credencial_dir()
    return dir_ / "credencial_frontal.png", dir_ / "credencial_reverso.png"

# === Rutas fijas ===

def get_bd_path():
    return get_data_db_dir() / "FamcDB.db"

def get_configuration():
    return get_data_dir() / "config.ini"

def get_backgrounds_dir():
    path = get_static_dir() / "backgrounds"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_background_front_side():
    return get_backgrounds_dir() / "front_side.png"

def get_background_back_side():
    return get_backgrounds_dir() / "back_side.png"


def get_layout_qr():
    qr_dir = get_static_dir() / "qr"
    qr_dir.mkdir(parents=True, exist_ok=True)
    return qr_dir / "whatsapp_qr.png"

# def _save_file_from_label( label, file_name, tipo):
#         """
#         Guarda la imagen desde un QLabel si existe. Pregunta si desea sobrescribir
#         en modo edición si el archivo ya existe.
#         """
#     if label.pixmap() is None:
#         return None
#
#     path = os.path.join("data", file_name, tipo)
#
#     if self.edition_mode and Path(path).exists():
#         response = QMessageBox.question(
#             self.mw.captureView,
#             f"Reemplazar {tipo}",
#             f"Ya existe una {tipo} para este folio.\n¿Deseas reemplazarla?",
#             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
#         )
#         if response != QMessageBox.StandardButton.Yes:
#             return path
#
#     save_image_from_label(label, path)
#     return path

