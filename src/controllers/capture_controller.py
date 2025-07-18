# src/controllers/capture_controller.py
import os
import cv2
from PySide6.QtCore import QObject, Signal
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from src.controllers.camera_controller import CameraController
from src.controllers.firma_controller import FirmaController
from src.controllers.previsualizacion_controller import PrevisualizacionController
from src.database.db_manager import DBManager
from src.utils.helpers import guardar_imagen_desde_label, recolectar_datos_formulario, guardar_archivo_temporal
from src.utils.rutas import get_temp_foto_path, get_temp_firma_path, get_firma_path, get_foto_path


from src.utils.rutas import get_temp_foto_path
import cv2

class CaptureController(QObject):
    credencial_actualizada = Signal()

    def __init__(self, main_window, ui , db_manager):
        super().__init__()
        self.mw = main_window
        self.ui = ui
        self.db = db_manager

        # Instancia del CameraController
        self.camera_ctrl = CameraController(self.ui.labelFoto, self.ui)
        self.ultima_ruta = None

        # Otros controladores
        self.firma_ctrl = FirmaController(parent_window=self.ui, label_firma=self.ui.labelFirma)
        self.preview_ctrl = PrevisualizacionController(self.ui)

        self.modo_edicion = False
        self.credencial_editando = None

        self._conectar_botones()

    def _conectar_botones(self):
        self.ui.btnIniciarFoto.clicked.connect(self.toggle_camera)
        self.ui.btnSubirFoto.clicked.connect(self.camera_ctrl.subir_foto_desde_archivo)
        self.ui.btnIniciarFirma.clicked.connect(self.firma_ctrl.manejar_estado_firma)
        self.ui.btnCapturarFirma.setVisible(False)

        # Conexión segura evitando warning
        try:
            self.ui.btnGuardarDatos.clicked.disconnect()
        except (TypeError, RuntimeError):
            pass
        self.ui.btnGuardarDatos.clicked.connect(self.guardar_credencial)

    def actualizar_db(self, nuevo_db_manager):

        # Metodo para actualizar el DBManager desde fuera, útil cuando cambia la base de datos.

        self.db = nuevo_db_manager

    def toggle_camera(self):
        self.camera_ctrl.manejar_estado_foto()

    def capturar_foto(self):
        ruta_foto = self.camera_ctrl.get_ruta_foto()
        if not ruta_foto or not Path(ruta_foto).exists():
            QMessageBox.warning(self.ui, "Error", "No se pudo capturar la imagen.")
            return

        self.ultima_ruta = ruta_foto

        pixmap = QPixmap(ruta_foto)
        self.ui.labelFoto.setPixmap(pixmap)
        self.ui.labelFoto.setScaledContents(True)
        self.ui.btnCapturarFoto.setEnabled(True)

    # Aquí seguirías con los métodos guardar_credencial, etc.

    # ... luego puedes conservar el resto de `guardar_credencial`, `_guardar_archivo_desde_label`, etc.


    def limpiar_formulario(self):
        self.camera_ctrl.detener_camara()
        for campo in [
            self.ui.nombre, self.ui.paterno, self.ui.materno, self.ui.curp,
            self.ui.fechaNacimiento, self.ui.calle, self.ui.lote,
            self.ui.manzana, self.ui.numExt, self.ui.numInt, self.ui.codigoPostal, self.ui.colonia,
            self.ui.municipio, self.ui.seccionElectoral, self.ui.genero,
            self.ui.celular, self.ui.email
        ]:
            campo.clear()
        self.ui.genero.clear()
        self.ui.genero.addItems(["", "Masculino", "Femenino"])

        self.ui.labelFoto.clear()
        self.ui.labelFoto.setText("Cámara no activa")
        self.ui.labelFoto.setStyleSheet("color: gray; font-style: italic;")

        self.ui.labelFirma.clear()


    def guardar_credencial(self):

        if not self.db:
            QMessageBox.critical(self.ui, "Error de base de datos",
                                 "No se ha establecido conexión con una base de datos.")
            return

        print(f"[DEBUG] Modo edición activo: {self.modo_edicion}")
        print(f"[DEBUG] Credencial en edición: {self.credencial_editando}")

        datos = recolectar_datos_formulario(self.ui)

        if not datos["Nombre"] or not datos["CURP"]:
            QMessageBox.warning(self.ui.viewCaptura, "Campos requeridos", "Nombre y CURP son obligatorios.")
            return

        if self.modo_edicion:
            self._guardar_edicion_credencial(datos)
            self.limpiar_formulario()
            self.ui.stackedWidget.setCurrentWidget(self.ui.viewHome)
            return

        folio = self._guardar_nueva_credencial(datos)
        datos["FolioId"] = folio

        try:
            ok_foto = guardar_archivo_temporal(
                get_temp_foto_path(), get_foto_path(folio), "Foto"
            )
            ok_firma = guardar_archivo_temporal(
                get_temp_firma_path(), get_firma_path(folio), "Firma"
            )

            if not ok_foto or not ok_firma:
                QMessageBox.warning(self.ui.viewCaptura, "Advertencia", "Faltan archivos por guardar.")

        except Exception as e:
            QMessageBox.critical(self.ui.viewCaptura, "Error al guardar archivos", str(e))
            return

        self.preview_ctrl.mostrar_credencial(datos)
        self.limpiar_formulario()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)

    def _guardar_nueva_credencial(self, datos):
        folio = self.db.generar_folio()
        self._guardar_credencial_base(folio, datos, is_update=False)
        return folio

    def _guardar_edicion_credencial(self, datos):
        folio = self.credencial_editando.FolioId
        self._guardar_credencial_base(folio, datos, is_update=True)

    def _guardar_credencial_base(self, folio, datos, is_update):
        ruta_foto = self._guardar_archivo_desde_label(self.ui.labelFoto, f"{folio}_foto.png", "foto")
        ruta_firma = self._guardar_archivo_desde_label(self.ui.labelFirma, f"{folio}_firma.png", "firma")

        datos.update({
            "ruta_foto": ruta_foto,
            "ruta_firma": ruta_firma,
        })
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

    def _guardar_archivo_desde_label(self, label, nombre_archivo, tipo):
        if label.pixmap() is None:
            return None

        ruta = os.path.join("data", tipo, nombre_archivo)
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)

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


    def _obtener_folio_actual(self):
        if self.modo_edicion and self.credencial_editando:
            return self.credencial_editando.FolioId
        return self.db.generar_folio()
