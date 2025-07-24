import os
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import cv2
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox

from src.utils.rutas import get_temp_foto_path

def recortar_frame_a_4_5(frame, salida_px=(800, 1000)):
    h, w = frame.shape[:2]
    target_ratio = 4 / 5

    # Calcular dimensiones centradas con proporción 4:5
    new_w = w
    new_h = int(w / target_ratio)

    if new_h > h:
        new_h = h
        new_w = int(h * target_ratio)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    cropped = frame[y1:y1 + new_h, x1:x1 + new_w]

    return cv2.resize(cropped, salida_px, interpolation=cv2.INTER_AREA)


def detectar_y_recortar_rostro(frame, label_foto):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    pad = int(0.4 * h)
    x1, y1 = max(x - pad, 0), max(y - pad, 0)
    x2, y2 = min(x + w + pad, frame.shape[1]), min(y + h + pad, frame.shape[0])

    rostro = frame[y1:y2, x1:x2]

    # Redimensionar al tamaño del QLabel
    size = label_foto.size()
    return cv2.resize(rostro, (size.width(), size.height()), interpolation=cv2.INTER_AREA)


def mejorar_imagen(frame):
    return cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

def dibujar_cruz_guia(frame):
    h, w = frame.shape[:2]
    color = (255, 0, 0)  # Azul en RGB
    grosor = 1

    # Línea horizontal
    cv2.line(frame, (0, h // 2), (w, h // 2), color, grosor)

    # Línea vertical
    cv2.line(frame, (w // 2, 0), (w // 2, h), color, grosor)

    return frame


class CameraController:
    def __init__(self, label_foto, parent_window):
        self.label = label_foto
        self.parent = parent_window
        self.cam = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.estado = 0  # 0 = Iniciar, 1 = Capturar, 2 = Repetir
        self.ultima_ruta_foto = ""
        self.indices_camaras = []

        # Solo una vez al inicializar
        indices = self.detectar_camaras_disponibles()
        self.parent.comboBoxCamera.clear()
        for i in indices:
            self.parent.comboBoxCamera.addItem(f"Cámara {i}", i)  # Aquí el segundo argumento es el dato real
        self.indices_camaras = indices

    def detectar_camaras_disponibles(self, max_camaras=3):
        camaras = []
        for i in range(max_camaras):
            cam = cv2.VideoCapture(i)
            if cam.isOpened():
                ret, frame = cam.read()
                if ret:
                    camaras.append(i)
                cam.release()
        return camaras

    def manejar_estado_foto(self):
        acciones = {
            0: self.iniciar_camara,
            1: self.capturar_foto,
            2: self.repetir_foto
        }
        acciones.get(self.estado, lambda: None)()

    def iniciar_camara(self):
        if not hasattr(self, 'indices_camaras') or not self.indices_camaras:
            QMessageBox.critical(self.parent, "Error", "No hay cámaras disponibles.")
            self._actualizar_boton("Error", False)
            return

        cam_id = self.parent.comboBoxCamera.currentData()  # <-- Obtén el dato del combo

        if cam_id is None:
            QMessageBox.critical(self.parent, "Error", "Selección de cámara inválida.")
            self._actualizar_boton("Error", False)
            return

        self.cam = cv2.VideoCapture(cam_id)

        if not self.cam.isOpened():
            QMessageBox.critical(self.parent, "Error", f"No se pudo abrir la cámara (ID: {cam_id}).")
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

            frame = recortar_frame_a_4_5(frame)
            frame = dibujar_cruz_guia(frame)

            self._mostrar_qimage_en_label(self._convertir_a_qimage(frame))

    def _convertir_a_qimage(self, frame_np):
        h, w, ch = frame_np.shape
        bytes_line = ch * w
        return QImage(frame_np.data, w, h, bytes_line, QImage.Format.Format_RGB888)

    def _mostrar_qimage_en_label(self, qimage):

        pixmap = QPixmap.fromImage(qimage)
        self.label.setPixmap(pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.label.setFixedSize(200, 250)  # 4:5 exacto

    def mostrar_en_label(self, ruta_imagen):
        if Path(ruta_imagen).exists():
            pixmap = QPixmap(ruta_imagen)
            self.label.setPixmap(pixmap.scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
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
