# src/controllers/edit_controller.py
from pathlib import Path
from shutil import copyfile

from PySide6.QtWidgets import QMessageBox
from src.database.db_manager import DBManager
from src.utils.helpers import save_image_from_label
from src.utils.rutas import get_temp_foto_path, get_temp_firma_path


class EditController:
    def __init__(self, main_window, capture_controller):
        self.mw = main_window
        self.ui = main_window.ui
        self.db = DBManager()
        self.capture_ctrl = capture_controller  # ✅ Reutiliza el que ya tiene estado y conexión real

    def _edit_user(self, index):
        """Cuando se hace doble clic sobre una fila."""
        row = index.row()
        model = self.ui.usersTableView.model()
        credential = model.get_filter(row)

        self.show_capture_form(credential)

    def _edit_selected(self):
        """Cuando se hace clic en el botón 'Editar'."""
        index = self.ui.usersTableView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.ui.viewCaptura, "Seleccionar usuario", "Selecciona una fila para editar.")
            return

        row = index.row()
        model = self.ui.usuariosVista.model()
        credential = model.obtener_datos_fila(row)

        self.show_capture_form(credential)

    def show_capture_form(self, credential):
        self.load_for_editing(credential)  # ✅ Esto ya limpia y carga
        self.ui.usersTableView.clearSelection()
        self.ui.stackedWidget.setCurrentWidget(self.ui.homeView)

    def load_for_editing(self, credential):
        self.capture_ctrl.clear_form()
        self.capture_ctrl.edition_mode = True
        self.capture_ctrl.credential_editing = True
        self.capture_ctrl.credential_editing = credential

        # Llenar campos
        self.ui.nombre.setText(credential.Nombre)
        self.ui.paterno.setText(credential.Paterno)
        self.ui.materno.setText(credential.Materno)
        self.ui.curp.setText(credential.CURP)
        self.ui.fechaNacimiento.setDate(credential.FechaNacimiento)
        self.ui.calle.setText(credential.Calle)
        self.ui.lote.setText(credential.Lote)
        self.ui.manzana.setText(credential.Manzana)
        self.ui.numExt.setText(credential.NumExterior)
        self.ui.numInt.setText(credential.NumInterior)
        self.ui.codigoPostal.setText(credential.CodigoPostal)
        self.ui.colonia.setText(credential.Colonia)
        self.ui.municipio.setText(credential.Municipio)
        self.ui.seccionElectoral.setText(str(credential.SeccionElectoral))
        self.ui.genero.setCurrentText(credential.Genero)
        self.ui.entidad.setText(credential.Entidad)
        self.ui.celular.setText(credential.Celular)
        self.ui.email.setText(credential.Email)

        # Foto
        if credential.RutaFoto and Path(credential.RutaFoto).exists():
            save_image_from_label(self.ui.labelPhoto, credential.RutaFoto, modo='cargar')
            copyfile(credential.RutaFoto, get_temp_foto_path())
            self.capture_ctrl.camera_ctrl.status = 2  # Repetir
            self.ui.startPhotoBtn.setText("Repetir")
        else:
            self.ui.labelPhoto.clear()
            self.ui.labelPhoto.setText("Cámara no activa")
            self.ui.labelPhoto.setStyleSheet("color: gray; font-style: italic;")
            self.capture_ctrl.camera_ctrl.status = 0
            self.ui.startPhotoBtn.setText("Iniciar cámara")

        # Firma
        if credential.RutaFirma and Path(credential.RutaFirma).exists():
            save_image_from_label(self.ui.labelFirma, credential.RutaFirma, modo='cargar')
            copyfile(credential.RutaFirma, get_temp_firma_path())

