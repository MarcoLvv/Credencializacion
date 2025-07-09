import sys
from pathlib import Path

def get_base_dir():
    """
    Devuelve la carpeta base del launcher (ya sea ejecutable o script .py).
    """
    if getattr(sys, 'frozen', False):  # Ejecutable creado con PyInstaller
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parents[2]  # Ajusta según dónde esté rutas.py

def get_data_dir():
    """
    Devuelve la carpeta 'data/' junto al launcher. La crea si no existe.
    """
    data_dir = get_base_dir() / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def get_foto_dir():
    foto_dir = get_data_dir() / "fotos"
    foto_dir.mkdir(parents=True, exist_ok=True)
    return foto_dir

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
    from tempfile import gettempdir
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
    return get_data_dir() / "credenciales.db"

def get_configuration():
    return get_data_dir() / "config.ini"

def get_layout_front():
    return get_data_dir() / "static" / "layout" / "front.png"

def get_layout_back():
    return get_data_dir() / "static" / "layout" / "back.png"

def get_layout_QR():
    return get_data_dir() / "static" / "qr" / "whatsapp.png"