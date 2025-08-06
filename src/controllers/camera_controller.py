import os

from src.utils.helpers import show_scaled_preview

os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import numpy as np
import cv2
from pathlib import Path

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox, QLabel

from src.utils.rutas import get_temp_foto_path
import logging

def process_frame_with_face(frame, label=None, already_rgb=False):
    print("[DEBUG] Procesando fotograma...")

    if not already_rgb:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        frame_rgb = frame

    cropped = detect_and_expand_face(frame_rgb, zoomout_factor=2.0)

    if cropped is None:
        print("[WARNING] No se detectó rostro, se usará la imagen completa.")
        return crop_to_4_5(frame_rgb)  # Imagen sin rostro, recortada estándar

    # Ya está con aspecto 3:4 y centrado. No hace falta center_face_vertically ni crop_to_aspect_ratio_centered
    enhanced = enhance_image(cropped)

    transparent = remove_background_mask(enhanced)
    if transparent is None:
        print("[WARNING] Falló eliminación de fondo, se usará recorte sin fondo.")
        return enhanced

    return transparent


def center_face_vertically(image, target_height):
    h, w = image.shape[:2]

    if h == target_height:
        return image

    elif h < target_height:
        # Centrar verticalmente con relleno (bordes negros)
        top = (target_height - h) // 2
        bottom = target_height - h - top
        return cv2.copyMakeBorder(image, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    else:
        # Si es más alta, solo recortar el centro vertical
        y1 = (h - target_height) // 2
        return image[y1:y1 + target_height, :]

def resize_to_aspect_ratio(image: np.ndarray, aspect_ratio: float = 3 / 2) -> np.ndarray:
    """
    Resizes the image to the given aspect ratio (default 4:3), maintaining the center.
    It will crop (not stretch) the image.
    """
    h, w = image.shape[:2]
    current_ratio = w / h

    if current_ratio > aspect_ratio:
        # Image is too wide; crop sides
        new_w = int(h * aspect_ratio)
        x1 = (w - new_w) // 2
        return image[:, x1:x1 + new_w]
    else:
        # Image is too tall; crop top and bottom
        new_h = int(w / aspect_ratio)
        y1 = (h - new_h) // 2
        return image[y1:y1 + new_h, :]

def detect_and_expand_face(image: np.ndarray, zoomout_factor=2.0) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        print("[ERROR] No se detectó ningún rostro.")
        return None

    x, y, w, h = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0]
    cx, cy = x + w // 2, y + h // 2

    expanded_w = int(w * zoomout_factor)
    expanded_h = int(h * zoomout_factor)

    x1 = max(0, cx - expanded_w // 2)
    y1 = max(0, cy - expanded_h // 2)
    x2 = min(image.shape[1], cx + expanded_w // 2)
    y2 = min(image.shape[0], cy + expanded_h // 2)

    crop = image[y1:y2, x1:x2]
    return crop_to_aspect(crop, aspect_ratio=3 / 4)




# Ajustar a aspecto 3:4 (ancho:alto) sin recortar
def pad_to_aspect(image, aspect_ratio=3/4):
    h, w = image.shape[:2]
    current_aspect = w / h

    if current_aspect > aspect_ratio:
        # Demasiado ancho → añadir bordes verticales
        new_h = int(w / aspect_ratio)
        pad = new_h - h
        top = pad // 2
        bottom = pad - top
        return cv2.copyMakeBorder(image, top, bottom, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    elif current_aspect < aspect_ratio:
        # Demasiado alto → añadir bordes horizontales
        new_w = int(h * aspect_ratio)
        pad = new_w - w
        left = pad // 2
        right = pad - left
        return cv2.copyMakeBorder(image, 0, 0, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    else:
        return image

def crop_to_aspect(image, aspect_ratio=3/4):
    h, w = image.shape[:2]
    current_aspect = w / h

    if current_aspect > aspect_ratio:
        # Demasiado ancho → recortar lados
        new_w = int(h * aspect_ratio)
        x1 = (w - new_w) // 2
        return image[:, x1:x1 + new_w]
    elif current_aspect < aspect_ratio:
        # Demasiado alto → recortar arriba y abajo
        new_h = int(w / aspect_ratio)
        y1 = (h - new_h) // 2
        return image[y1:y1 + new_h, :]
    else:
        return image



#def crop_to_4_5(image, output_size=(800, 1000)):
def crop_to_4_5(image, output_size=(800, 1000)):
    h, w = image.shape[:2]
    target_ratio = 4 / 5

    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        new_h = h
    else:
        new_w = w
        new_h = int(w / target_ratio)

    x1 = (w - new_w) // 2
    y1 = (h - new_h) // 2
    cropped = image[y1:y1 + new_h, x1:x1 + new_w]

    if output_size:
        return cv2.resize(cropped, output_size, interpolation=cv2.INTER_AREA)
    return cropped

def crop_to_aspect_ratio_centered(image: np.ndarray, target_ratio: float = 4 / 3) -> np.ndarray:
    """
    Crops the image to a given aspect ratio (width/height) from the center,
    with priority to preserve the top (head).
    """
    h, w = image.shape[:2]
    desired_w = int(h * target_ratio)
    desired_h = int(w / target_ratio)

    if w / h > target_ratio:
        # Too wide, crop width
        x_start = (w - desired_w) // 2
        cropped = image[:, x_start:x_start + desired_w]
    else:
        # Too tall, crop height with bias to include top of head
        y_center = h // 2
        y_start = max(0, y_center - desired_h // 2 - int(0.1 * desired_h))  # slight shift upward
        y_end = y_start + desired_h
        if y_end > h:
            y_end = h
            y_start = h - desired_h
        cropped = image[y_start:y_end, :]

    return cropped


def enhance_image(image):
    image = cv2.convertScaleAbs(image, alpha=1.2, beta=15)
    kernel = np.array([[0, -1, 0], [-1, 5.2, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def remove_background_mask(frame: np.ndarray) -> np.ndarray:
    """
    Removes background using an elliptical mask centered on the face area.
    Returns an RGBA image with transparent background.
    """
    if frame is None:
        print("[ERROR] Frame vacío en remove_background_mask.")
        return None
    if not isinstance(frame, np.ndarray):
        print("[ERROR] Frame no es un np.ndarray.")
        return None

    h, w = frame.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    center_x, center_y = w // 2, int(h * 0.45)
    axes_length = (int(w * 0.45), int(h * 0.6))

    cv2.ellipse(mask, (center_x, center_y), axes_length, 0, 0, 360, 255, -1)

    if frame.shape[2] == 3:
        frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    else:
        frame_rgba = frame.copy()

    frame_rgba[:, :, 3] = mask
    return frame_rgba.copy()

def _convert_to_qimage(image_np: np.ndarray) -> QImage:
    height, width = image_np.shape[:2]

    if image_np.shape[2] == 4:
        image_rgba = cv2.cvtColor(image_np, cv2.COLOR_BGRA2RGBA)
        return QImage(
            image_rgba.data, width, height, QImage.Format.Format_RGBA8888
        )
    else:
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        return QImage(
            image_rgb.data, width, height, QImage.Format.Format_RGB888
        )

def draw_guide_cross(frame):
    h, w = frame.shape[:2]
    color = (255, 0, 0)  # Azul en RGB
    thickness = 1

    # Línea horizontal
    cv2.line(frame, (0, h // 2), (w, h // 2), color, thickness)

    # Línea vertical
    cv2.line(frame, (w // 2, 0), (w // 2, h), color, thickness)

    return frame

def detect_available_cameras(max_camaras=3):
    cameras = []
    for i in range(max_camaras):
        cam = cv2.VideoCapture(i)
        if cam.isOpened():
            ret, frame = cam.read()
            if ret:
                cameras.append(i)
            cam.release()
    return cameras


# Configura logs en entorno compilado
logging.basicConfig(
    filename="camera_controller.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

class CameraController:
    def __init__(self, label_foto, parent_window):
        self.label = label_foto
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

    def manage_photo_state(self):
        logging.debug("Estado actual: %s", self.status)
        actions = {
            0: self.start_camera,
            1: self.take_photo,
            2: self.repeat_photo
        }
        actions.get(self.status, lambda: None)()

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

        self.cam = cv2.VideoCapture(cam_id)
        logging.debug("cv2.VideoCapture(%s) -> %s", cam_id, self.cam)

        if not self.cam.isOpened():
            QMessageBox.critical(self.parent, "Error", f"No se pudo abrir la cámara (ID: {cam_id}).")
            self._update_button("Error", False)
            logging.error("No se pudo abrir la cámara con ID %s", cam_id)
            return

        self.timer.start(30)
        self.status = 1
        self._update_button("Capturar", True)
        logging.info("Cámara iniciada correctamente")

    def take_photo(self):
        if self.last_frame is None:
            logging.error("No hay frame disponible para capturar")
            return

        processed = process_frame_with_face(self.last_frame, self.label, already_rgb=True)
        if processed is None:
            logging.error("No se pudo procesar la imagen")
            return

        temp_photo_path = get_temp_foto_path()

        try:
            if processed.shape[2] == 4:
                frame_to_save = cv2.cvtColor(processed, cv2.COLOR_RGBA2BGR)
            else:
                frame_to_save = cv2.cvtColor(processed, cv2.COLOR_RGB2BGR)

            success = cv2.imwrite(str(temp_photo_path), frame_to_save, [cv2.IMWRITE_JPEG_QUALITY, 95])
            logging.info("Imagen guardada: %s en %s", success, temp_photo_path)

            self.last_photo_path = str(temp_photo_path)
            show_scaled_preview(self.last_photo_path, self.label)
            self.stop_camera()
            self.status = 2
            self._update_button("Repetir", True)
        except Exception as e:
            logging.exception("Error al guardar imagen capturada")

    def repeat_photo(self):
        self.last_photo_path = ""
        self.start_camera()

    def _get_current_frame(self):
        if self.cam:
            ret, frame = self.cam.read()
            if ret:
                return frame
        return None

    def _update_frame(self):
        if self.cam and self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_cropped = crop_to_4_5(frame_rgb)
                self.last_frame = frame_rgb.copy()
                self.show_image_no_borders(frame_cropped)
            else:
                logging.warning("Frame no leído desde la cámara")
        else:
            logging.debug("_update_frame llamado sin cámara activa")

    def upload_photo_from_file(self):
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
        enhanced_image = process_frame_with_face(image_upload, self.label, already_rgb=True)
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

    def prepare_capture_state(self):
        self.stop_camera()
        self.last_photo_path = ""
        self.status = 0
        self.label.clear()
        self.label.setText("Cámara no activa")
        self.label.setStyleSheet("color: gray; font-style: italic;")
        self._update_button("Iniciar cámara", True)

    def _update_button(self, text, enabled=True):
        self.parent.startPhotoBtn.setText(text)
        self.parent.startPhotoBtn.setEnabled(enabled)

    def get_photo_path(self):
        return self.last_photo_path

    def stop_camera(self):
        logging.debug("Cerrando cámara y deteniendo timer")
        self.timer.stop()
        if self.cam:
            self.cam.release()
            self.cam = None

    def show_pixmap_scaled(self, pixmap: QPixmap, label: QLabel):
        """Escala y muestra el QPixmap en el QLabel manteniendo calidad y proporción."""
        if pixmap is None or label is None:
            return

        scaled = pixmap.scaled(
            label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        label.setPixmap(scaled)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_image_from_qimage(self, qimage: QImage, label: QLabel):
        """Convierte QImage a QPixmap y lo muestra en el label."""
        pixmap = QPixmap.fromImage(qimage)
        self.show_pixmap_scaled(pixmap, label)

    def show_image_from_path(self, image_path: str, label: QLabel):
        """Carga imagen desde archivo y la muestra escalada."""
        if Path(image_path).exists():
            pixmap = QPixmap(image_path)
            self.show_pixmap_scaled(pixmap, label)

    def show_image_from_array(self, frame_np: np.ndarray, label: QLabel):
        """Convierte np.ndarray (RGB/BGR/RGBA) a QImage y la muestra en el label."""
        if frame_np is None or not isinstance(frame_np, np.ndarray):
            return

        frame_np = np.ascontiguousarray(frame_np)  # ✅ necesario para evitar BufferError
        h, w = frame_np.shape[:2]
        channels = frame_np.shape[2] if frame_np.ndim == 3 else 1

        if channels == 4:
            qimage = QImage(frame_np.data, w, h, frame_np.strides[0], QImage.Format.Format_RGBA8888)
        elif channels == 3:
            qimage = QImage(frame_np.data, w, h, frame_np.strides[0], QImage.Format.Format_RGB888)
        else:
            # Imagen en escala de grises
            qimage = QImage(frame_np.data, w, h, frame_np.strides[0], QImage.Format.Format_Grayscale8)

        self.show_image_from_qimage(qimage, label)

    def show_image_in_label(self, image_path):
        if Path(image_path).exists():
            pixmap = QPixmap(str(image_path))
            self.label.setPixmap(pixmap)
            # self.label.setPixmap(pixmap.scaled(
            #     self.label.size(),
            #     Qt.AspectRatioMode.KeepAspectRatio,
            #     Qt.TransformationMode.SmoothTransformation
            # ))

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
        label_size = self.label.size()
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
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # print("Label size:", label_size.width(), label_size.height())
        # print("Pixmap size before scaling:", pixmap.width(), pixmap.height())

        scaled_pixmap = pixmap.scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.label.setPixmap(scaled_pixmap)
