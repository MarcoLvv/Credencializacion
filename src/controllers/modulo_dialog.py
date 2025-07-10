# controllers/modulo_dialog.py

import re
from PySide6.QtWidgets import QDialog, QMessageBox
from src.views.modulo import Ui_Dialog
from src.utils.config_manager import set_module_id


class ModuloDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Configuración de Módulo")
        self.ui.lineModulo.setPlaceholderText("Ej. M01")

    def accept(self):
        modulo = self.ui.lineModulo.text().strip().upper()

        if not re.match(r"^M\d{2}$", modulo):
            QMessageBox.warning(self, "Formato inválido", "El módulo debe tener el formato M00 a M99.")
            return

        try:
            set_module_id(modulo)
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el módulo: {e}")
