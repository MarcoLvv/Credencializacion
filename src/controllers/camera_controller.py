# src/controllers/camera.py

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
        self.estado = 0  # 0 = Iniciar cámara, 1 = Capturar, 2 = Repetir
        self.ultima_ruta_foto = ""

    def manejar_estado_foto(self):
        if self.estado == 0:
            self.iniciar_camara()
        elif self.estado == 1:
            self.capturar_foto()
        elif self.estado == 2:
            self.repetir_foto()

    def iniciar_camara(self):
        self.cam = cv2.VideoCapture(1)
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

        frame = recortar_frame_a_4_5(frame)
        frame = mejorar_imagen(frame)
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
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.label.setPixmap(pixmap.scaled(
                self.label.width(),
                self.label.height()
            ))

    def detener_camara(self):
        self.timer.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    def mostrar_en_label(self, ruta_imagen):
        if not Path(ruta_imagen).exists():
            return
        pixmap = QPixmap(ruta_imagen)
        self.label.setPixmap(pixmap.scaled(
            self.label.width(),
            self.label.height()
        ))

    def mostrar_en_label_desde_array(self, frame_np):
        """Muestra en el QLabel una imagen OpenCV (ndarray en RGB)."""
        if frame_np is None:
            return

        alto, ancho, canales = frame_np.shape
        bytes_por_linea = canales * ancho
        qimage = QImage(
            frame_np.data,
            ancho,
            alto,
            bytes_por_linea,
            QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

    def get_ruta_foto(self):
        return self.ultima_ruta_foto

    def preparar_estado_captura(self):
        """⚙️ Reinicia la cámara al estado inicial sin iniciarla."""
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

    def preparar_estado_captura(self):
        # Metodo para dejar el botón y cámara en estado inicial, sin abrir la cámara.
        self.detener_camara()
        self.ultima_ruta_foto = ""
        self.estado = 0
        self.label.clear()
        self._actualizar_boton("Iniciar cámara", True)

    def subir_foto_desde_archivo(self):
        """Abre un diálogo para seleccionar una foto del sistema de archivos."""
        ruta, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Seleccionar foto",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if ruta:
            imagen = cv2.imread(ruta)

            if imagen is None:
                print("[ERROR] No se pudo leer la imagen seleccionada.")
                return

            # Convertir a RGB
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

            # Recortar a relación 4:5
            imagen_crop = recortar_frame_a_4_5(imagen_rgb)

            # Mejorar imagen si quieres (opcional)
            imagen_mejorada = mejorar_imagen(imagen_crop)

            # Mostrar en label
            self.mostrar_en_label_desde_array(imagen_mejorada)

            ruta = get_temp_foto_path()
            cv2.imwrite(str(ruta), cv2.cvtColor(imagen_mejorada, cv2.COLOR_RGB2BGR))
            self.frame_capturado = imagen_mejorada
            self.ruta_foto_capturada = ruta

            # Guardar imagen como "capturada"
            self.frame_capturado = imagen_mejorada

            # Cambiar estado del botón a "Repetir"
            self.estado = 2
            self._actualizar_boton("Repetir", enabled=True)