# controllers/modulo_dialog.py

import re
from PySide6.QtWidgets import QDialog, QMessageBox

from src.database.db_manager import DBManager
from src.utils.rutas import get_bd_path
from src.views.modulo import Ui_Dialog
from src.utils.config_manager import set_module_id

def crear_base_si_no_existe():
    db_path = get_bd_path()
    if not db_path.exists():
        print("⚙️ No se encontró la base de datos, creando una nueva...")
        db = DBManager()
        db.crear_tablas()  # Este metodo debe asegurarse de crear todas las tablas necesarias
        print(f"✅ Base de datos creada en: {db_path}")
    else:
        print(f"📂 Base de datos ya existente : {db_path}.")

class ModuloDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Configuración de Módulo")
        self.ui.lineModulo.setPlaceholderText("Ej. M01")


    def accept(self):
        modulo = self.ui.lineModulo.text().strip().upper()
        #crear_base_si_no_existe()
        if not re.match(r"^M\d{2}$", modulo):
            QMessageBox.warning(self, "Formato inválido", "El módulo debe tener el formato M00 a M99.")
            return

        try:
            set_module_id(modulo)
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el módulo: {e}")
