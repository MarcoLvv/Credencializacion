import pandas as pd
from datetime import datetime, date

def normalize_credential_data(raw_data: dict) -> dict:
    """Limpia, normaliza y asegura los campos obligatorios de una credencial."""

    # Limpieza general de strings excepto FechaNacimiento
    data = {
        k: ("" if pd.isna(v) or v is None else str(v).strip())
        for k, v in raw_data.items()
        if k != "FechaNacimiento"
    }

    # Validación/Asignación de FechaNacimiento
    fecha = raw_data.get("FechaNacimiento")
    if not isinstance(fecha, date):
        raise ValueError("FechaNacimiento debe ser un objeto date válido.")
    data["FechaNacimiento"] = fecha

    # Valores por defecto
    defaults = {
        "RutaFoto": "",
        "RutaFirma": "",
        "RutaQR": "",
        "Responsable": "",
        "NumImpresion": 0,
        "VecesImpresa": 0,
        #"Entregada": True,
        "FechaAlta": date.today()
    }

    for key, value in defaults.items():
        data.setdefault(key, value)

    return data

def convert_dates_in_dict(data: dict, date_fields: list):
    """
    Convierte las cadenas de fecha en objetos datetime.date en los campos indicados.
    Si no puede convertir, asigna None.
    """
    for field in date_fields:
        val = data.get(field)
        if val is None:
            continue
        if isinstance(val, str):
            try:
                data[field] = datetime.strptime(val, "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠️ Fecha inválida para campo {field}: {val}")
                data[field] = None
        elif not isinstance(val, date):
            # Si no es string ni date, asignamos None para evitar errores
            data[field] = None


def convert_booleans_in_dict(data: dict, bool_fields: list):
    """
    Convierte los campos indicados en booleanos.
    Acepta strings como "0", "1", "true", "false", números 0/1.
    """
    for field in bool_fields:
        val = data.get(field)
        if isinstance(val, str):
            val = val.strip().lower()
            if val in ("1", "true", "sí", "si"):
                data[field] = True
            elif val in ("0", "false", "no"):
                data[field] = False
            else:
                data[field] = False  # Valor por defecto si es ambiguo
        elif isinstance(val, int):
            data[field] = bool(val)
        elif isinstance(val, bool):
            continue
        else:
            data[field] = False  # Valor por defecto si no es reconocible

