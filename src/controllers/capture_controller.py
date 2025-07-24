# Refactorizado `capture_controller.py`

from pathlib import Path
import os

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from src.controllers.camera_controller import CameraController
from src.controllers.firma_controller import FirmaController
from src.controllers.previsualizacion_controller import PrevisualizacionController
from src.utils.helpers import guardar_imagen_desde_label, recolectar_datos_formulario, guardar_archivo_temporal, \
    signal_disconnect
from src.utils.rutas import (
    get_temp_foto_path, get_temp_firma_path, get_firma_path,
    get_foto_path
)

class CaptureController(QObject):
    credencial_actualizada = Signal()

    def __init__(self, main_window, ui, db_manager, preview_ctrl):

        super().__init__()
        self.mw = main_window
        self.ui = ui
        self.db = db_manager

        self.camera_ctrl = CameraController(self.ui.labelFoto, self.ui)
        self.firma_ctrl = FirmaController(parent_window=self.ui, label_firma=self.ui.labelFirma)
        self.preview_ctrl = preview_ctrl


        self.modo_edicion = False
        self.credencial_editando = None

        # En tu clase CaptureController:
        self.guardado_conectado = False

        self._conectar_botones()



    def _conectar_botones(self):
        self.ui.btnIniciarFoto.clicked.connect(self.camera_ctrl.manejar_estado_foto)
        self.ui.btnSubirFoto.clicked.connect(self.camera_ctrl.subir_foto_desde_archivo)
        self.ui.btnIniciarFirma.clicked.connect(self.firma_ctrl.manejar_estado_firma)
        self.ui.btnCapturarFirma.setVisible(False)

        if self.guardado_conectado:
            try:
                self.ui.btnGuardarDatos.clicked.disconnect(self.guardar_credencial)
            except Exception:
                pass

        self.ui.btnGuardarDatos.clicked.connect(self.guardar_credencial)
        self.guardado_conectado = True

    def actualizar_db(self, nuevo_db_manager):
        self.db = nuevo_db_manager

    def limpiar_formulario(self):
        self.camera_ctrl.detener_camara()
        for campo in [
            self.ui.nombre, self.ui.paterno, self.ui.materno, self.ui.curp,
            self.ui.fechaNacimiento, self.ui.calle, self.ui.lote,
            self.ui.manzana, self.ui.numExt, self.ui.numInt, self.ui.codigoPostal,
            self.ui.colonia, self.ui.municipio, self.ui.seccionElectoral,
            self.ui.genero, self.ui.celular, self.ui.email
        ]:
            campo.clear()

        self.ui.genero.clear()
        self.ui.genero.addItems(["", "Masculino", "Femenino"])

        for label, text in [(self.ui.labelFoto, "Cámara no activa"), (self.ui.labelFirma, "")]:
            label.clear()
            label.setText(text)
            label.setStyleSheet("color: gray; font-style: italic;")

    def guardar_credencial(self):
        if not self.db:
            QMessageBox.critical(self.ui, "Error de base de datos", "No se ha establecido conexión con la base de datos.")
            return

        datos = recolectar_datos_formulario(self.ui)

        if not datos["Nombre"] or not datos["CURP"]:
            QMessageBox.warning(self.ui.viewCaptura, "Campos requeridos", "Nombre y CURP son obligatorios.")
            return

        if self.modo_edicion and self.credencial_editando:
            self._guardar_edicion_credencial(datos)
        else:

            folio = self._guardar_nueva_credencial(datos)
            datos_completos = self.db.obtener_credencial_por_folio(folio)
            self.preview_ctrl.mostrar_credencial(datos_completos)

        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)

        self.limpiar_formulario()

    def _guardar_nueva_credencial(self, datos):
        folio = self.db.generar_folio()
        self._guardar_credencial_base(folio, datos, is_update=False)
        return folio

    def _guardar_edicion_credencial(self, datos):
        folio = self.credencial_editando.FolioId
        self._guardar_credencial_base(folio, datos, is_update=True)
        datos_completos = self.db.obtener_credencial_por_folio(folio)
        self.preview_ctrl.mostrar_credencial(datos_completos)  # FALTABA ESTO
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)

    def _guardar_credencial_base(self, folio, datos, is_update):
        ruta_foto = guardar_archivo_temporal(get_temp_foto_path(), get_foto_path(folio), "Foto")
        ruta_firma = guardar_archivo_temporal(get_temp_firma_path(), get_firma_path(folio), "Firma")

        datos.update({"ruta_foto": ruta_foto, "ruta_firma": ruta_firma})

        try:
            if is_update:
                self.db.actualizar_credencial(folio, **datos)
                QMessageBox.information(self.mw.viewCaptura, "Actualizado", f"Credencial {folio} editada correctamente.")
            else:
                self.db.insertar_credencial(**datos)
                QMessageBox.information(self.mw.viewCaptura, "Guardado", f"Credencial {folio} guardada correctamente.")
            self.credencial_actualizada.emit()
        except Exception as e:
            QMessageBox.critical(self.mw.viewCaptura, "Error", f"No se pudo guardar: {e}")

        return datos

    def _guardar_archivo_desde_label(self, label, nombre_archivo, tipo):
        if label.pixmap() is None:
            return None

        ruta = os.path.join("data", nombre_archivo, tipo)

        if self.modo_edicion and Path(ruta).exists():
            respuesta = QMessageBox.question(
                self.mw.viewCaptura,
                f"Reemplazar {tipo}",
                f"Ya existe una {tipo} para este folio.\n¿Deseas reemplazarla?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta != QMessageBox.StandardButton.Yes:
                return ruta

        guardar_imagen_desde_label(label, ruta)
        return ruta
