# src/controllers/capture_controller.py

import os

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


class CaptureController(QObject):
    credencial_actualizada = Signal()

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        self.ui = main_window.ui
        self.db = DBManager()
        self.camera = CameraController(self.ui.labelFoto, self.mw)
        self.firma_ctrl = FirmaController(
            parent_window=self.mw,
            label_firma=self.ui.labelFirma
        )
        self.preview_ctrl = PrevisualizacionController(self.ui)
        #self.credencial_actualizada.connect(self.mw.load_table)

        self.modo_edicion = False
        self.credencial_editando = None

        self._conectar_botones()

    def _conectar_botones(self):
        self.ui.btnIniciarFoto.clicked.connect(self.camera.iniciar_camara)
        self.ui.btnIniciarFirma.clicked.connect(self.firma_ctrl.iniciar_capturar_firma)
        self.ui.btnCapturarFoto.clicked.connect(self._capturar_foto_ui)
        self.ui.btnCapturarFirma.clicked.connect(self._capturar_y_mostrar_firma)
        try:
            self.ui.btnGuardarDatos.clicked.disconnect()
        except TypeError:
            pass
        self.ui.btnGuardarDatos.clicked.connect(self.guardar_credencial)

    
    def _capturar_foto_ui(self):
        folio = self._obtener_folio_actual()
        ruta = self.camera.capturar_foto()
        if not ruta:
            QMessageBox.warning(self.ui, "Foto", "No se pudo capturar la foto.")

    def _capturar_y_mostrar_firma(self):
        ruta_firma = self.firma_ctrl.capturar_firma()
        if ruta_firma:
            pixmap = QPixmap(ruta_firma)
            self.ui.labelFirma.setPixmap(pixmap)
            self.ui.labelFirma.setScaledContents(True)
        else:
            QMessageBox.warning(self.ui, "Firma", "No se pudo capturar o mostrar la firma.")

    def limpiar_formulario(self):
        for campo in [
            self.ui.nombre, self.ui.paterno, self.ui.materno, self.ui.curp,
            self.ui.calle, self.ui.lote, self.ui.manzana, self.ui.numExt,
            self.ui.numInt, self.ui.codigoPostal, self.ui.colonia,
            self.ui.municipio, self.ui.seccionElectoral, self.ui.genero,
            self.ui.celular, self.ui.email
        ]:
            campo.clear()

        self.ui.labelFoto.clear()
        self.ui.labelFirma.clear()

    def guardar_credencial(self):
        print(f"[DEBUG] Modo edición activo: {self.modo_edicion}")
        print(f"[DEBUG] Credencial en edición: {self.credencial_editando}")

        datos = recolectar_datos_formulario(self.ui)

        if not datos["Nombre"] or not datos["CURP"]:
            QMessageBox.warning(self.mw, "Campos requeridos", "Nombre y CURP son obligatorios.")
            return

        if self.modo_edicion:
            self._guardar_edicion_credencial(datos)
            self.limpiar_formulario()
            self.ui.stackedWidget.setCurrentWidget(self.ui.viewHome)
            return

        folio = self._guardar_nueva_credencial(datos)
        datos["FolioId"] = folio

        # Guardar imágenes definitivas
        try:
            ok_foto = guardar_archivo_temporal(
                get_temp_foto_path(), get_foto_path(folio), "Foto"
            )
            ok_firma = guardar_archivo_temporal(
                get_temp_firma_path(), get_firma_path(folio), "Firma"
            )

            if not ok_foto or not ok_firma:
                QMessageBox.warning(self.mw, "Advertencia", "Faltan archivos por guardar.")

        except Exception as e:
            QMessageBox.critical(self.mw, "Error al guardar archivos", str(e))
            return

        # Mostrar previsualización y limpiar
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
                QMessageBox.information(self.mw, "Actualizado", f"Credencial {folio} editada correctamente.")
            else:
                self.db.insertar_credencial(**datos)
                QMessageBox.information(self.mw, "Guardado", f"Credencial {folio} guardada correctamente.")

            self.credencial_actualizada.emit()  # ✅ emitir señal para actualizar tabla

        except Exception as e:
            QMessageBox.critical(self.mw, "Error", f"No se pudo guardar: {e}")


    def _guardar_archivo_desde_label(self, label, nombre_archivo, tipo):
        if label.pixmap() is None:
            return None

        ruta = os.path.join("data", tipo, nombre_archivo)
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)

        if self.modo_edicion and Path(ruta).exists():
            respuesta = QMessageBox.question(
                self.ui,
                f"Reemplazar {tipo}",
                f"Ya existe una {tipo} para este folio.\n¿Deseas reemplazarla?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if respuesta != QMessageBox.StandardButton.Yes:
                return ruta

        guardar_imagen_desde_label(label, ruta)
        return ruta

    def cargar_para_edicion(self, credencial):
        self.limpiar_formulario()
        self.modo_edicion = True
        self.credencial_editando = credencial

        self.ui.nombre.setText(credencial.Nombre)
        self.ui.paterno.setText(credencial.Paterno)
        self.ui.materno.setText(credencial.Materno)
        self.ui.curp.setText(credencial.CURP)
        self.ui.calle.setText(credencial.Calle)
        self.ui.lote.setText(credencial.Lote)
        self.ui.manzana.setText(credencial.Manzana)
        self.ui.numExt.setText(credencial.NumExterior)
        self.ui.numInt.setText(credencial.NumInterior)
        self.ui.codigoPostal.setText(credencial.CodigoPostal)
        self.ui.colonia.setText(credencial.Colonia)
        self.ui.municipio.setText(credencial.Municipio)
        self.ui.seccionElectoral.setText(credencial.SeccionElectoral)
        self.ui.genero.setText(credencial.GeneroId)
        self.ui.celular.setText(credencial.Celular)
        self.ui.email.setText(credencial.Email)

        if credencial.RutaFoto and Path(credencial.RutaFoto).exists():
            guardar_imagen_desde_label(self.ui.labelFoto, credencial.RutaFoto, modo='cargar')
        if credencial.RutaFirma and Path(credencial.RutaFirma).exists():
            guardar_imagen_desde_label(self.ui.labelFirma, credencial.RutaFirma, modo='cargar')

    def _obtener_folio_actual(self):
        if self.modo_edicion and self.credencial_editando:
            return self.credencial_editando.FolioId
        return self.db.generar_folio()
