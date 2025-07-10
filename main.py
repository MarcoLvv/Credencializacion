import sys
import os
import json
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog
from src.controllers.main_controller import VistaPrincipal
from src.controllers.modulo_dialog import ModuloDialog
from src.database.db_manager import init_db
from src.utils.config_manager import CONFIG_PATH, get_module_id


def crear_config_si_no_existe():
    """Crea el archivo de configuración si no existe, pidiendo módulo al usuario."""
    if not os.path.exists(CONFIG_PATH):
        modulo = ""
        while not modulo:
            modulo = input("Ingrese el código del módulo (ej. M01): ").strip().upper()
            if not modulo:
                print("El código de módulo no puede estar vacío.")
        try:
            with open(CONFIG_PATH, "w") as f:
                json.dump({"modulo": modulo}, f)
            print(f"Configuración creada en {CONFIG_PATH} con módulo: {modulo}")
        except Exception as e:
            print(f"[ERROR] No se pudo crear la configuración: {e}")
            sys.exit(1)



def main():
    # Crear carpeta 'data' si no existe
    os.makedirs("data", exist_ok=True)

    # Crear configuración inicial si es necesario
    if not os.path.exists(CONFIG_PATH) or not get_module_id():
        app = QApplication(sys.argv)  # Inicializar Qt antes de mostrar el diálogo
        dlg = ModuloDialog()
        if dlg.exec() != QDialog.DialogCode.Accepted:
            QMessageBox.critical(None, "Error", "Debe ingresar un módulo válido para continuar.")
            sys.exit(1)

    # Inicializar la base de datos
    try:
        init_db()
        print("Tablas creadas.")
    except Exception as e:
        print(f"[ERROR] Error al inicializar la base de datos: {e}")
        sys.exit(1)

    app = QApplication(sys.argv)
    # with open("./estilo.qss", "r") as f:
    #     style = f.read()
    #     app.setStyleSheet(style)
    with open("estilo.qss", "r", encoding="utf-8") as f:
        style = f.read()
        app.setStyleSheet(style)

    window = VistaPrincipal()
    window.show()

    try:
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Error crítico", f"Ocurrió un error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
