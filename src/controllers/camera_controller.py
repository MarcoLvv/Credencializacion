import cv2
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog

from src.utils.rutas import get_temp_foto_path
from src.workers.worker import mejorar_imagen, recortar_frame_a_4_5


class CameraController:
    def __init__(self, label_foto, parent_window):
        self.label = label_foto
        self.parent = parent_window
        self.cam = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.estado = 0  # 0 = Iniciar, 1 = Capturar, 2 = Repetir
        self.ultima_ruta_foto = ""

    def detectar_camaras_disponibles(self, max_camaras=3):
        camaras = []
        for i in range(max_camaras):
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                cam.release()
                camaras.append(i)
        return camaras

    def manejar_estado_foto(self):
        acciones = {
            0: self.iniciar_camara,
            1: self.capturar_foto,
            2: self.repetir_foto
        }
        acciones.get(self.estado, lambda: None)()

    def iniciar_camara(self):
        cam_idx = self.parent.comboBoxCamera.currentIndex()
        cam_id = self.indices_camaras[cam_idx] if hasattr(self, 'indices_camaras') else 0
        self.cam = cv2.VideoCapture(cam_id)

        if not self.cam.isOpened():
            self._actualizar_boton("Error", False)
            return
        self.timer.start(30)
        self.estado = 1
        self._actualizar_boton("Capturar", True)

    def capturar_foto(self):
        frame = self._obtener_frame_actual()
        if frame is None:
            return

        frame = mejorar_imagen(recortar_frame_a_4_5(frame))
        ruta = get_temp_foto_path()
        cv2.imwrite(str(ruta), frame)
        self.ultima_ruta_foto = str(ruta)

        self.mostrar_en_label(self.ultima_ruta_foto)
        self.detener_camara()
        self.estado = 2
        self._actualizar_boton("Repetir", True)

    def repetir_foto(self):
        self.ultima_ruta_foto = ""
        self.iniciar_camara()

    def subir_foto_desde_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self.parent.viewCaptura,
            "Seleccionar foto",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if ruta:
            imagen = cv2.imread(ruta)
            if imagen is None:
                print("[ERROR] No se pudo leer la imagen seleccionada.")
                return

            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            imagen_mejorada = mejorar_imagen(recortar_frame_a_4_5(imagen_rgb))

            self.mostrar_en_label_desde_array(imagen_mejorada)

            ruta_salida = get_temp_foto_path()
            cv2.imwrite(str(ruta_salida), cv2.cvtColor(imagen_mejorada, cv2.COLOR_RGB2BGR))
            self.ultima_ruta_foto = str(ruta_salida)
            self.estado = 2
            self._actualizar_boton("Repetir", True)

    def _obtener_frame_actual(self):
        if self.cam:
            ret, frame = self.cam.read()
            if ret:
                return frame
        return None

    def _update_frame(self):
        frame = self._obtener_frame_actual()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self._mostrar_qimage_en_label(self._convertir_a_qimage(frame))

    def _convertir_a_qimage(self, frame_np):
        h, w, ch = frame_np.shape
        bytes_line = ch * w
        return QImage(frame_np.data, w, h, bytes_line, QImage.Format_RGB888)

    def _mostrar_qimage_en_label(self, qimage):
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap.scaled(
            self.label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def mostrar_en_label(self, ruta_imagen):
        if Path(ruta_imagen).exists():
            pixmap = QPixmap(ruta_imagen)
            self.label.setPixmap(pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def mostrar_en_label_desde_array(self, frame_np):
        if frame_np is not None:
            self._mostrar_qimage_en_label(self._convertir_a_qimage(frame_np))

    def detener_camara(self):
        self.timer.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    def preparar_estado_captura(self):
        self.detener_camara()
        self.ultima_ruta_foto = ""
        self.estado = 0
        self.label.clear()
        self.label.setText("Cámara no activa")
        self.label.setStyleSheet("color: gray; font-style: italic;")
        self._actualizar_boton("Iniciar cámara", True)

    def _actualizar_boton(self, texto, habilitado=True):
        self.parent.btnIniciarFoto.setText(texto)
        self.parent.btnIniciarFoto.setEnabled(habilitado)

    def get_ruta_foto(self):
        return self.ultima_ruta_foto
