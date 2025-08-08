import os

from src.utils.camera_utils import detectar_rostro, detect_available_cameras, crop_to_4_5, process_frame_with_face
from src.utils.helpers import show_scaled_preview

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import logging

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox, QLabel

from src.utils.rutas import get_temp_foto_path, heearcascade_face_path

import numpy as np
import cv2
# Configura logs en entorno compilado
logging.basicConfig(
    filename="camera_controller.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class CameraController:
    def __init__(self, parent_window, label_foto):
        self.photo_label = label_foto
        self.parent = parent_window
        self.cam = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.status = 0  # 0 = Iniciar, 1 = Capturar, 2 = Repetir
        self.last_photo_path = ""
        self.camera_index = []
        self.last_frame = None  # Para guardar el último frame mostrado

        try:
            indexes = detect_available_cameras()
            self.parent.comboBoxCamera.clear()
            for i in indexes:
                self.parent.comboBoxCamera.addItem(f"Cámara {i}", i)
            self.camera_index = indexes
            logging.info("Cámaras detectadas: %s", indexes)
        except Exception as e:
            logging.exception("Error al detectar cámaras")

    def prepare_photo_state(self):
        self.stop_camera()
        self.last_photo_path = ""
        self.status = 0
        self.photo_label.clear()
        self.photo_label.setText("Cámara no activa")
        self.photo_label.setStyleSheet("color: gray; font-style: italic;")
        self._update_button("Iniciar cámara", True)

    def manage_photo_state(self):
        logging.debug("Estado actual: %s", self.status)
        actions = {
            0: self.start_camera,
            1: self.take_photo,
            2: self.repeat_photo
        }
        actions.get(self.status, lambda: None)()

    def _update_button(self, text, enabled=True):
        self.parent.startPhotoBtn.setText(text)
        self.parent.startPhotoBtn.setEnabled(enabled)

    def start_camera(self):
        logging.debug("Intentando iniciar cámara")

        if not hasattr(self, 'camera_index') or not self.camera_index:
            QMessageBox.critical(self.parent, "Error", "No hay cámaras disponibles.")
            self._update_button("Error", False)
            logging.error("No hay cámaras disponibles")
            return

        cam_id = self.parent.comboBoxCamera.currentData()
        if cam_id is None:
            QMessageBox.critical(self.parent, "Error", "Selección de cámara inválida.")
            self._update_button("Error", False)
            logging.error("Selección de cámara inválida")
            return

        self.cam = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
        logging.debug("cv2.VideoCapture(%s) -> %s", cam_id, self.cam)

        if not self.cam.isOpened():
            QMessageBox.critical(self.parent, "Error", f"No se pudo abrir la cámara (ID: {cam_id}).")
            self._update_button("Error", False)
            logging.error("No se pudo abrir la cámara con ID %s", cam_id)
            return

        # Conectar el QTimer si no se ha conectado antes
        if not hasattr(self, 'timer') or self.timer is None:
            self.timer = QTimer(self.parent)
            self.timer.timeout.connect(self._update_frame)
            logging.debug("QTimer creado y conectado a _update_frame")

        self.timer.start(30)
        logging.info("QTimer iniciado con intervalo de 30 ms")

        self.status = 1
        self._update_button("Capturar", True)
        logging.info("Cámara iniciada correctamente con ID %s", cam_id)

    def stop_camera(self):
        logging.debug("Cerrando cámara y deteniendo timer")
        self.timer.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    def _update_frame(self):
        logging.debug("Llamado a _update_frame")
        if self.cam and self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                logging.debug("Frame leído correctamente")
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_cropped = crop_to_4_5(frame_rgb)
                self.last_frame = frame_rgb.copy()
                logging.debug("last_frame actualizado")
                self.show_image_no_borders(frame_cropped)
            else:
                logging.warning("Frame no leído desde la cámara")
        else:
            logging.debug("self.cam no está inicializado o no está abierto")

    def take_photo(self):
        logging.debug("Entrando a take_photo(), last_frame: %s", type(self.last_frame))
        if self.last_frame is None:
            logging.error("No hay frame disponible para capturar")
            return

        processed = process_frame_with_face(self.last_frame, self.photo_label, already_rgb=True)
        if processed is None:
            logging.error("No se pudo procesar la imagen")
            return

        temp_photo_path = get_temp_foto_path()
        logging.debug("Intentando guardar en path: %s", temp_photo_path)
        logging.debug("Existe directorio padre: %s", temp_photo_path.parent.exists())
        logging.debug("Es escribible: %s", os.access(str(temp_photo_path.parent), os.W_OK))

        try:
            if processed.shape[2] == 4:
                frame_to_save = cv2.cvtColor(processed, cv2.COLOR_RGBA2BGR)
            else:
                frame_to_save = cv2.cvtColor(processed, cv2.COLOR_RGB2BGR)

            # Prueba: intentar crear un archivo de texto en el mismo lugar
            try:
                temp_photo_path.parent.mkdir(parents=True, exist_ok=True)
                test_file = temp_photo_path.parent / "test.txt"
                with open(test_file, "w", encoding="utf-8") as f:
                    f.write("prueba de escritura")
                logging.debug("Se pudo escribir test.txt correctamente")
            except Exception as e:
                logging.exception("Fallo al escribir test.txt en temp dir")

            logging.debug("processed shape: %s, dtype: %s", processed.shape, processed.dtype)

            logging.info(f"Procesamiento completo. Intentando guardar imagen en: {temp_photo_path}")

            self.save_photo(processed, temp_photo_path)
            #success = cv2.imwrite(str(temp_photo_path), frame_to_save, [cv2.IMWRITE_JPEG_QUALITY, 95])

            self.last_photo_path = str(temp_photo_path)
            show_scaled_preview(self.last_photo_path, self.photo_label)
            self.stop_camera()
            self.status = 2
            self._update_button("Repetir", True)
        except Exception as e:
            logging.exception("Error al guardar imagen capturada")

    def repeat_photo(self):
        self.last_photo_path = ""
        self.start_camera()

    def save_photo(self, image: np.ndarray, path: str):
        logging.debug(f"Guardando imagen en: {path}")
        try:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(path, image)
            logging.debug("Imagen guardada exitosamente.")
        except Exception as e:
            logging.error(f"Error al guardar la imagen: {e}")

    def upload_photo_from_file(self):
        self.stop_camera()
        file_photo_path, _ = QFileDialog.getOpenFileName(
            self.parent.captureView,
            "Seleccionar foto",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_photo_path:
            return

        image_upload = cv2.imread(file_photo_path)
        if image_upload is None:
            QMessageBox.warning(self.parent, "Error", "No se pudo abrir la imagen.")
            logging.warning("No se pudo abrir la imagen cargada desde archivo")
            return

        image_upload = cv2.cvtColor(image_upload, cv2.COLOR_BGR2RGB)
        enhanced_image = process_frame_with_face(image_upload, self.photo_label, already_rgb=True)
        if enhanced_image is None:
            logging.warning("Imagen subida no fue procesada")
            return

        self.show_image_no_borders(enhanced_image)
        output_file_photo_path = get_temp_foto_path()

        image_to_save = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(str(output_file_photo_path), image_to_save, [cv2.IMWRITE_JPEG_QUALITY, 95])

        self.last_photo_path = str(output_file_photo_path)
        self.status = 2
        self._update_button("Repetir", True)

    # def get_photo_path(self):
    #     return self.last_photo_path

    def _crop_to_label_ratio(self, image: np.ndarray, target_ratio: float) -> np.ndarray:
        h, w = image.shape[:2]
        current_ratio = w / h

        if current_ratio > target_ratio:
            # Imagen demasiado ancha, recortar ancho
            new_w = int(h * target_ratio)
            x1 = (w - new_w) // 2
            return image[:, x1:x1 + new_w]
        else:
            # Imagen demasiado alta, recortar altura
            new_h = int(w / target_ratio)
            y1 = (h - new_h) // 2
            return image[y1:y1 + new_h, :]

    def show_image_no_borders(self, image: np.ndarray):
        label_size = self.photo_label.size()
        label_ratio = label_size.width() / label_size.height()

        cropped_image = self._crop_to_label_ratio(image, label_ratio)

        h, w = cropped_image.shape[:2]
        channels = cropped_image.shape[2] if cropped_image.ndim == 3 else 1

        if channels == 4:
            qimage = QImage(cropped_image.data, w, h, cropped_image.strides[0], QImage.Format.Format_RGBA8888)
        elif channels == 3:
            qimage = QImage(cropped_image.data, w, h, cropped_image.strides[0], QImage.Format.Format_RGB888)
        else:
            qimage = QImage(cropped_image.data, w, h, cropped_image.strides[0], QImage.Format.Format_Grayscale8)

        pixmap = QPixmap.fromImage(qimage)
        self.photo_label.setScaledContents(False)
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        scaled_pixmap = pixmap.scaled(
                self.photo_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.photo_label.setPixmap(scaled_pixmap)


