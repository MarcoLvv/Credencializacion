# src/controllers/main_controller.py
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QMainWindow, QHeaderView

from src.controllers.capture_controller import CaptureController
from src.controllers.edit_controller import EditController
from src.controllers.previsualizacion_controller import PrevisualizacionController
from src.database.db_manager import DBManager
from src.delegates.action_delegate import ActionDelegate
from src.models.usuarios_table_model import UsuariosTableModel
from src.views.ventana_principal import Ui_MainWindow


class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DBManager()
        # Controladores
        # Crear primero el controlador de captura sin conectar la señal
        self.capture_ctrl = CaptureController(self)  # Pasa self (QMainWindow)
        # Luego crear el controlador de edición
        self.edit_ctrl = EditController(self, self.capture_ctrl)
        # Ahora conectar la señal, ya que edit_ctrl está listo
        self.preview_ctrl = PrevisualizacionController(self.ui)

        self.capture_ctrl.credencial_actualizada.connect(self.load_table)

        self.ui.searchBar.textChanged.connect(self.load_table)

        # Conectar botones principales
        self.ui.btnCapturar.clicked.connect(self._mostrar_formulario_captura)
        self.ui.btnInicio.clicked.connect(self._mostrar_home)
        #self.ui.btnEditar.clicked.connect(self._mostrar_usuarios)
        #self.ui.btnVer.clicked.connect(self._ver_credencial)

        self.load_table()
        # Mostrar pantalla inicial
        self._mostrar_home()

    def load_table(self):
        """Carga la tabla filtrando por texto si se proporciona."""
        search_text = self.ui.searchBar.text()
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

        # 🔘 Asignar el ActionDelegate a la columna de acciones (última columna, índice 6)
        self.action_delegate = ActionDelegate(self.ui.usuariosVista)
        acciones_columna = 6  # Verifica que sea la correcta según tu modelo

        self.ui.usuariosVista.setItemDelegateForColumn(acciones_columna, self.action_delegate)

        # 🔗 Conectar señales
        self.action_delegate.editarClicked.connect(self._editar_usuario_por_fila)
        self.action_delegate.verClicked.connect(self._ver_usuario_por_fila)

    def _editar_usuario_por_fila(self, fila):
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)
        self.edit_ctrl._mostrar_formulario_captura(credencial)  # Asegúrate que esta funcione correctamente
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def _ver_usuario_por_fila(self, fila):
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)
        self.preview_ctrl.mostrar_credencial(credencial)
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)

    def _ver_credencial(self):
        index = self.ui.usuariosVista.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.ui.usuariosVista, "Ver credencial", "Selecciona un usuario para ver su credencial.")
            return

        row = index.row()
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(row)

        self.preview_ctrl.mostrar_credencial(credencial)
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)


    def _mostrar_formulario_captura(self):
        # 🔽 Asegura que siempre se inicie una nueva captura
        self.capture_ctrl.modo_edicion = False
        self.capture_ctrl.credencial_editando = None

        self.capture_ctrl.limpiar_formulario()
        self.ui.usuariosVista.clearSelection()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def _mostrar_home(self):
        header = self.ui.usuariosVista.horizontalHeader()
        #model = self.ui.viewHome.model()
        self.ui.usuariosVista.verticalHeader().setVisible(False)

        # Columna 0: ajusta solo al contenido
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        # Columnas 1 a 5: que se expandan para ocupar el espacio restante
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

        self.ui.stackedWidget.setCurrentWidget(self.ui.viewHome)

    def _mostrar_usuarios(self):
        # El controlador de edición lo gestiona automáticamente.
        time.sleep(0.1)  # Esperar 100ms por si el archivo aún se está escribiendo
        
        self.edit_ctrl.load_table()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)