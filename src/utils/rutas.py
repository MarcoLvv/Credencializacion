import sys
import tempfile
from pathlib import Path
from tempfile import gettempdir


#Metodo para obtener la carpeta base
def get_base_dir():
    """Devuelve la carpeta base (modo ejecutable o desarrollo)."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path.cwd()

#Metodo para obtener la carpeta data
def get_data_dir():
    """Crea y devuelve la carpeta /data base del sistema."""
    data_dir = get_base_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

#Metodo para obtener la ruta a los algoritmos Haar para la deteccion de rostros
def heearcascade_face_path():
    return get_data_dir() / "haarcascade"

#Metodo para obtener la ruta a las exportaciones
def get_exportaciones_dir():
    """Crea y devuelve la carpeta /data/exportaciones"""
    path = get_data_dir() / "exportaciones"
    path.mkdir(parents=True, exist_ok=True)
    return path

# === Carpetas por tipo ===
#Metodo para obtener ruta a estilos
def get_styles():
    return get_data_dir() /"resources" / "styles" / "styles.qss"

#Metodo para obtener ruta a la carpeta de las bases de datos
def get_data_db_dir():
    path = get_data_dir() / "bases"
    path.mkdir(parents=True, exist_ok=True)
    return path

#Metodo para obtener ruta a la carpeta de excel
def get_excel_dir():
    path = get_data_dir() / "excel"
    path.mkdir(parents=True, exist_ok=True)
    return path

#Metodo para obtener ruta a los archivos estaticos
def get_static_dir():
    path = get_data_dir() / "static"
    path.mkdir(parents=True, exist_ok=True)
    return path

#Metodo para obtener ruta de los iconos
def get_icons_path(nombre_icono: str) -> Path:
    """Devuelve la ruta absoluta de un icono dentro de /data/icons."""
    return get_data_dir() / "icons" / nombre_icono

#Metodo para obtener ruta a la carpeta de fotos.
def get_foto_dir():
    path = get_data_dir() / "fotos"
    path.mkdir(parents=True, exist_ok=True)
    return path

#Metodo para obtener ruta a la carpeta de firmas
def get_firma_dir():
    path = get_data_dir() / "firmas"
    path.mkdir(parents=True, exist_ok=True)
    return path

#Metodo para obtener ruta a la carpeta de temporales
def get_temp_dir():
    path = get_data_dir() / "temp"
    path.mkdir(parents=True, exist_ok=True)
    return path

# === Archivos temporales individuales ===

def get_temp_path_qlabel(nombre_archivo: str) -> Path:
    temp_dir = Path(tempfile.gettempdir()) / "credenciales_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / nombre_archivo

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

def get_background_front_side(front_side_background_path : str) -> Path:
    return get_backgrounds_dir() / f"{front_side_background_path}.png"

def get_background_back_side(back_side_background_path : str) -> Path :
    return get_backgrounds_dir() / f"{back_side_background_path}.png"


def get_layout_qr():
    qr_dir = get_static_dir() / "qr"
    qr_dir.mkdir(parents=True, exist_ok=True)
    return qr_dir / "whatsapp_qr.png"
0

