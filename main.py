# main.py

import sys
import os
import json
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog
from src.controllers.main_controller import VistaPrincipal
from src.controllers.modulo_dialog import ModuloDialog
from src.utils.config_manager import CONFIG_PATH, get_module_id
from src.utils.rutas import get_styles


def main():
    # Crear carpeta 'data' si no existe
    os.makedirs("data", exist_ok=True)

    app = QApplication(sys.argv)  # ✅ Solo una instancia de QApplication

    # Crear configuración inicial si es necesario
    if not os.path.exists(CONFIG_PATH) or not get_module_id():
        dlg = ModuloDialog()
        if dlg.exec() != QDialog.DialogCode.Accepted:
            QMessageBox.critical(None, "Error", "Debe ingresar un módulo válido para continuar.")
            sys.exit(1)

    # Aplicar estilo (una vez que ya se validó la configuración)
    with open(get_styles(), encoding="utf-8") as f:
        style = f.read()
        app.setStyleSheet(style)

    # Mostrar ventana principal
    window = VistaPrincipal()
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Error crítico", f"Ocurrió un error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
