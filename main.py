# main.py

import os
import sys

# ✅ Antes de cualquier import de PySide6
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
#os.environ["QT_SCALE_FACTOR_ROUNDING_POLICY"] = "PassThrough"


from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog

QApplication.setAttribute(Qt.ApplicationAttribute.AA_DisableHighDpiScaling, True)

from src.controllers.main_controller import MainWindow
from src.controllers.modulo_dialog import ModuloDialog
from src.utils.config_manager import CONFIG_PATH, get_module_id
from src.utils.rutas import get_styles

def main():
    # Crear carpeta 'data' si no existe
    os.makedirs("data", exist_ok=True)

    app = QApplication(sys.argv)

    if not os.path.exists(CONFIG_PATH) or not get_module_id():
        dlg = ModuloDialog()
        if dlg.exec() != QDialog.DialogCode.Accepted:
            QMessageBox.critical(None, "Error", "Debe ingresar un módulo válido para continuar.")
            sys.exit(1)

    with open(get_styles(), encoding="utf-8") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Error crítico", f"Ocurrió un error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
