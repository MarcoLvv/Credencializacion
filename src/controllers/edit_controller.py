# src/controllers/edit_controller.py

from PySide6.QtWidgets import QMessageBox
from src.database.db_manager import DBManager
from src.models.usuarios_table_model import UsuariosTableModel


class EditController:
    def __init__(self, main_window, capture_controller):
        self.mw = main_window
        self.ui = main_window.ui
        self.db = DBManager()
        self.capture_ctrl = capture_controller  # ✅ Reutiliza el que ya tiene estado y conexión real

        # Conectar eventos de edición
        #self.ui.searchBar.textChanged.connect(self.load_table)
        self.ui.btnEditar.clicked.connect(self._editar_seleccionado)
        #desconectar_btn_guardar(self.ui)

        # Cargar datos al inicio
        self.load_table()

        #self.ui.usuariosVista.doubleClicked.connect(self.edit_ctrl._editar_usuario)

    def load_table(self):
        """Carga la tabla filtrando por texto si se proporciona."""
        search_text = self.ui.searchBar.text().strip()
        credenciales = self.db.obtener_todas()

        if search_text:
            search_text_lower = search_text.lower()
            credenciales = [
                c for c in credenciales
                if search_text_lower in c.Nombre.lower()
                or search_text_lower in c.Paterno.lower()
                or search_text_lower in c.Materno.lower()
                or search_text_lower in c.CURP.lower()
                or search_text_lower in c.FolioId.lower()
            ]

        model = UsuariosTableModel(credenciales)
        self.ui.usuariosVista.setModel(model)

    def _editar_usuario(self, index):
        """Cuando se hace doble clic sobre una fila."""
        row = index.row()
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(row)

        self._mostrar_formulario_captura(credencial)

    def _editar_seleccionado(self):
        """Cuando se hace clic en el botón 'Editar'."""
        index = self.ui.usuariosVista.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.ui.viewCaptura, "Seleccionar usuario", "Selecciona una fila para editar.")
            return

        row = index.row()
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(row)

        self._mostrar_formulario_captura(credencial)

    def _mostrar_formulario_captura(self, credencial):
        self.capture_ctrl.cargar_para_edicion(credencial)  # ✅ Esto ya limpia y carga
        self.ui.usuariosVista.clearSelection()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

