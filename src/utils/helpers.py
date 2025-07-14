from datetime import date
from pathlib import Path
from PySide6.QtGui import QPixmap

import shutil

def guardar_imagen_desde_label(label, path, modo='guardar'):
    if modo == 'guardar':
        pixmap = label.pixmap()
        if pixmap:
            pixmap.save(path)
    elif modo == 'cargar':
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

def guardar_archivo_temporal(origen: Path, destino: Path, nombre: str):
    if not origen.exists():
        print(f"[ADVERTENCIA] {nombre} temporal no encontrada.")
        return False

    shutil.copy(origen, destino)
    print(f"[DEBUG] {nombre} guardada: {destino}")

    origen.unlink(missing_ok=True)  # Limpieza
    return True


# src/utils/helpers.py

def desconectar_senal(widget, senal, funcion=None):
    """
    Desconecta una señal de un widget de forma segura.

    Parámetros:
    - widget: el objeto que emite la señal (ej. QPushButton).
    - senal: la señal a desconectar (ej. widget.clicked).
    - funcion: opcional, si solo deseas desconectar una función específica.
    """
    try:
        if funcion:
            senal.disconnect(funcion)
        else:
            senal.disconnect()
    except (TypeError, RuntimeError):
        pass  # La señal no estaba conectada o ya fue eliminada

def desconectar_btn_guardar(ui):
    try:
        if hasattr(ui, "btnGuardarDatos"):
            ui.btnGuardarDatos.clicked.disconnect()
    except (TypeError, RuntimeWarning):
        pass


def recolectar_datos_formulario(ui):
    fecha_qt = ui.fechaNacimiento.date()
    fechaNacimiento = date(fecha_qt.year(), fecha_qt.month(), fecha_qt.day())

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
        "SeccionElectoral": ui.seccionElectoral.text().strip(),
        "Genero": ui.genero.currentText(),
        "Celular": ui.celular.text().strip(),
        "Email": ui.email.text().strip()

    }
