import os
import sys
from pathlib import Path
from tempfile import gettempdir


def get_base_dir():
    """
    Devuelve la carpeta base del launcher (ya sea ejecutable o script).
    - En modo PyInstaller (producción): la carpeta del ejecutable.
    - En modo desarrollo: el cwd desde donde se ejecuta el script (usualmente main.py).
    """
    if getattr(sys, 'frozen', False):  # Ejecutable con PyInstaller
        return Path(sys.executable).parent
    return Path.cwd()



def get_data_dir():
    """
    Devuelve la carpeta 'data/' junto al launcher. La crea si no existe.
    """

    data_dir = get_base_dir() / "data" / "bases"
    data_temp = get_base_dir() / "data" / "temp"
    data_temp.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_bases_disponibles():
    directorio = get_data_dir()
    return [f for f in os.listdir(directorio) if f.endswith(".db")]

def get_excel_dir():
    excel_dir = get_data_dir() / "excel"
    excel_dir.mkdir(parents=True, exist_ok=True)

    return excel_dir
def get_foto_dir():
    foto_dir = get_data_dir() / "fotos"
    foto_dir.mkdir(parents=True, exist_ok=True)
    return foto_dir

def get_icons_dir():
    icons_dir = get_data_dir() / "icons"
    icons_dir.mkdir(parents=True, exist_ok=True)
    return icons_dir

def get_firma_dir():
    firma_dir = get_data_dir() / "firmas"
    firma_dir.mkdir(parents=True, exist_ok=True)
    return firma_dir

def get_temp_firma_path():
    temp_dir = get_data_dir() / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / "temp_firma.png"

def get_temp_foto_path():
    temp_dir = get_data_dir() / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / "temp_foto.png"

def get_temp_credencial_dir():
    path = Path(gettempdir()) / "credenciales_temp"
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_temp_credencial_paths():
    dir_ = get_temp_credencial_dir()
    return dir_ / "credencial_frontal.png", dir_ / "credencial_reverso.png"

def get_temp_foto_path():
    return get_data_dir() / "temp" / "temp_foto.png"

def get_temp_firma_path():
    return get_data_dir() / "temp" / "temp_firma.png"

def get_foto_path(folio_id: str):
    path = get_foto_dir() / f"{folio_id}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def get_firma_path(folio_id: str):
    path = get_firma_dir() / f"{folio_id}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


# Rutas Fijas para layouts.

def get_bd_path():
    return get_data_dir()

def get_configuration():
    return get_data_dir() / "config.ini"

def get_layout_front():
    return get_data_dir() / "static" / "layout" / "front.png"

def get_layout_back():
    return get_data_dir() / "static" / "layout" / "back.png"

def get_layout_QR():
    return get_data_dir() / "static" / "qr" / "whatsapp.png"