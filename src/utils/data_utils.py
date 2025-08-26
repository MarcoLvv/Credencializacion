import pandas as pd
from datetime import datetime, date

from pandas import isna


def normalize_credential_data(raw_data: dict) -> dict:
    """
    Limpia y normaliza los datos de una fila de Excel/CSV.
    - Strings se limpian
    - None o NaN se convierten en ""
    - FechaNacimiento y FechaAlta se convierten a datetime.date
      si faltan, se asigna date.today()
    - Se agregan valores por defecto para ciertos campos
    """
    # Limpieza de strings y conversión de NaN a ""
    data = {
        k: ("" if pd.isna(v) or v is None else str(v).strip())
        for k, v in raw_data.items()
        if k not in ("FechaNacimiento", "FechaAlta")
    }

    def parse_date(value, field_name):
        """Convierte a date; si está vacío o mal, asigna hoy"""
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except Exception:
                print(f"⚠️ {field_name} en fila tiene formato incorrecto. Se asignará fecha hoy.")
                return date.today()
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return date.today()
        raise ValueError(f"{field_name} debe ser date o string con formato YYYY-MM-DD")

    # FechaNacimiento
    fecha_nac_raw = raw_data.get("FechaNacimiento")
    data["FechaNacimiento"] = parse_date(fecha_nac_raw, "FechaNacimiento")

    # FechaAlta
    fecha_alta_raw = raw_data.get("FechaAlta")
    data["FechaAlta"] = parse_date(fecha_alta_raw, "FechaAlta") if fecha_alta_raw else date.today()

    # Valores por defecto
    defaults = {
        "RutaFoto": "",
        "RutaFirma": "",
        "Responsable": "",
        "VecesImpresa": 0,
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

