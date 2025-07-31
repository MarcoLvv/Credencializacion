# capture_controller.py


from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox

from src.controllers.camera_controller import CameraController
from src.controllers.signature_controller import SignatureController

from src.utils.helpers import (
    collect_data_form,
    save_temporary_file,
)

from src.utils.rutas import (
    get_temp_foto_path,
    get_temp_firma_path,
    get_firma_path,
    get_foto_path,
)


class CaptureController(QObject):
    updated_credential = Signal()

    def __init__(self, main_window, ui, db_manager, preview_ctrl):
        super().__init__()
        self.mw = main_window
        self.ui = ui
        self.db = db_manager
        self.preview_ctrl = preview_ctrl

        self.camera_ctrl = CameraController(self.ui.labelPhoto, self.ui)
        self.signature_ctrl = SignatureController(self.ui, self.ui.labelSignature)

        self.edition_mode = False
        self.credential_editing = None
        self.saved_connected = False

        self._connect_buttons()

    def _connect_buttons(self):
        """Conecta los botones del formulario con sus respectivos controladores."""
        self.ui.startPhotoBtn.clicked.connect(self.camera_ctrl.manage_photo_state)
        self.ui.uploadPhotoBtn.clicked.connect(self.camera_ctrl.upload_photo_from_file)
        self.ui.startSignatureBtn.clicked.connect(self.signature_ctrl.manage_signature_state)
        self.ui.uploadSignatureBtn.setVisible(False)

        if self.saved_connected:
            try:
                self.ui.saveDataBtn.clicked.disconnect(self.save_credential)
            except Exception:
                pass

        self.ui.saveDataBtn.clicked.connect(self.save_credential)
        self.saved_connected = True

    def clear_form(self):
        """Limpia el formulario de captura y detiene la cámara."""
        self.camera_ctrl.stop_camera()

        campos = [
            self.ui.nombre, self.ui.paterno, self.ui.materno, self.ui.curp,
            self.ui.fechaNacimiento, self.ui.calle, self.ui.lote,
            self.ui.manzana, self.ui.numExt, self.ui.numInt, self.ui.codigoPostal,
            self.ui.colonia, self.ui.municipio, self.ui.entidad, self.ui.seccionElectoral,
            self.ui.genero, self.ui.celular, self.ui.email
        ]
        for campo in campos:
            campo.clear()

        self.ui.municipio.setText("Cuajimalpa")
        self.ui.entidad.setText("Ciudad De Mexico")

        self.ui.genero.clear()
        self.ui.genero.addItems(["", "Masculino", "Femenino"])

        # Etiquetas de foto y firma
        for label, texto in [(self.ui.labelPhoto, "Cámara no activa"), (self.ui.labelSignature, "")]:
            label.clear()
            label.setText(texto)
            label.setStyleSheet("color: gray; font-style: italic;")

    def save_credential(self):
        """Guarda una credencial nueva o actualiza una existente."""
        if not self.db:
            QMessageBox.critical(self.ui, "Error de base de datos", "No se ha establecido conexión con la base de datos.")
            return

        data = collect_data_form(self.ui)

        if not data["Nombre"] or not data["CURP"]:
            QMessageBox.warning(self.ui.captureView, "Campos requeridos", "Nombre y CURP son obligatorios.")
            return

        if self.edition_mode and self.credential_editing:
            self._save_edition_credential(data)
        else:
            folio = self._save_new_credential(data)
            complete_data = self.db.get_credential_by_folio(folio)
            self.preview_ctrl.show_credential(complete_data)

        self.ui.stackedWidget.setCurrentWidget(self.ui.credentialView)
        self.clear_form()

    def _save_new_credential(self, data):
        """Genera folio y guarda una nueva credencial."""
        folio = self.db.generate_folio()
        self._save_credential_files_db(folio, data, is_update=False)
        return folio

    def _save_edition_credential(self, data):
        """Guarda los cambios en una credencial existente."""
        folio = self.credential_editing.FolioId
        self._save_credential_files_db(folio, data, is_update=True)
        complete_data = self.db.get_credential_by_folio(folio)
        self.preview_ctrl.show_credential(complete_data)
        self.ui.stackedWidget.setCurrentWidget(self.ui.credentialView)

    def _save_credential_files_db(self, folio, data, is_update):
        """Guarda los archivos (foto/firma) y actualiza la base de datos."""
        photo_path = save_temporary_file(get_temp_foto_path(), get_foto_path(folio), "Foto")
        signature_path = save_temporary_file(get_temp_firma_path(), get_firma_path(folio), "Firma")

            
        data.update({
            "RutaFoto": photo_path,
            "RutaFirma": signature_path
        })

        try:
            if is_update:
                self.db.actualizar_credencial(folio, **data)
                QMessageBox.information(self.mw.captureView, "Actualizado", f"Credencial {folio} editada correctamente.")
            else:
                self.db.insertar_credencial(**data)
                QMessageBox.information(self.mw.captureView, "Guardado", f"Credencial {folio} guardada correctamente.")
            self.updated_credential.emit()
        except Exception as e:
            QMessageBox.critical(self.mw.captureView, "Error", f"No se pudo guardar: {e}")

        return data


