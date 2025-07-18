# src/controllers/edit_controller.py
from pathlib import Path

from PySide6.QtWidgets import QMessageBox
from src.database.db_manager import DBManager
from src.models.usuarios_table_model import UsuariosTableModel
from src.utils.helpers import guardar_imagen_desde_label


class EditController:
    def __init__(self, main_window, capture_controller):
        self.mw = main_window
        self.ui = main_window.ui
        self.db = DBManager()
        self.capture_ctrl = capture_controller  # ✅ Reutiliza el que ya tiene estado y conexión real

        # Conectar eventos de edición
        #self.ui.searchBar.textChanged.connect(self.load_table)
        #self.ui.btnEditar.clicked.connect(self._editar_seleccionado)
        #desconectar_btn_guardar(self.ui)


        #self.ui.usuariosVista.doubleClicked.connect(self.edit_ctrl._editar_usuario)

    def _editar_usuario(self, index):
        """Cuando se hace doble clic sobre una fila."""
        row = index.row()
        model = self.ui.usuariosVista.model()
        credencial = model.get_filter(row)

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
        self.cargar_para_edicion(credencial)  # ✅ Esto ya limpia y carga
        self.ui.usuariosVista.clearSelection()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def cargar_para_edicion(self, credencial):
        self.capture_ctrl.limpiar_formulario()
        self.modo_edicion = True
        self.credencial_editando = credencial

        # Llenar campos
        self.ui.nombre.setText(credencial.Nombre)
        self.ui.paterno.setText(credencial.Paterno)
        self.ui.materno.setText(credencial.Materno)
        self.ui.curp.setText(credencial.CURP)
        self.ui.fechaNacimiento.setDate(credencial.FechaNacimiento)
        self.ui.calle.setText(credencial.Calle)
        self.ui.lote.setText(credencial.Lote)
        self.ui.manzana.setText(credencial.Manzana)
        self.ui.numExt.setText(credencial.NumExterior)
        self.ui.numInt.setText(credencial.NumInterior)
        self.ui.codigoPostal.setText(credencial.CodigoPostal)
        self.ui.colonia.setText(credencial.Colonia)
        self.ui.municipio.setText(credencial.Municipio)
        self.ui.seccionElectoral.setText(credencial.SeccionElectoral)
        self.ui.genero.setCurrentText(credencial.Genero)
        self.ui.celular.setText(credencial.Celular)
        self.ui.email.setText(credencial.Email)

        # Foto
        if credencial.RutaFoto and Path(credencial.RutaFoto).exists():
            guardar_imagen_desde_label(self.ui.labelFoto, credencial.RutaFoto, modo='cargar')
            self.capture_ctrl.camera_ctrl.estado = 2  # Repetir
            self.ui.btnIniciarFoto.setText("Repetir")
        else:
            self.ui.labelFoto.clear()
            self.ui.labelFoto.setText("Cámara no activa")
            self.ui.labelFoto.setStyleSheet("color: gray; font-style: italic;")
            self.capture_ctrl.camera_ctrl.estado = 0
            self.ui.btnIniciarFoto.setText("Iniciar cámara")

        # Firma
        if credencial.RutaFirma and Path(credencial.RutaFirma).exists():
            guardar_imagen_desde_label(self.ui.labelFirma, credencial.RutaFirma, modo='cargar')

