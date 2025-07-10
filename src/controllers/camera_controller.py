from pathlib import Path
import cv2
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QImage
from src.database.db_manager import DBManager
from src.integrations.camera import CameraPreview
from src.utils.rutas import get_firma_dir, get_temp_foto_path


class CameraController:
    """
    • Controla la vista previa (CameraPreview).
    • Permite capturar la imagen tal cual se ve en el QLabel:
      - Recorta el rostro con OpenCV (zoom automático).
      - Guarda la imagen en data/fotos/{consecutivo}.png.
      - Actualiza el QLabel con la foto guardada.
    """
    def __init__(self, target_label, main_window):
        self.mw = main_window
        self.preview      = CameraPreview(target_label)
        self.label_foto   = target_label
        self.db           = DBManager()

        self.foto_dir = get_firma_dir()
        self.foto_dir.mkdir(parents=True, exist_ok=True)
        self.ultima_ruta = None

        # Clasificador de rostros
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    # ---------- control cámara ----------
    def iniciar_camara(self):
        # Limpiar QLabel para eliminar imagen anterior
        self.label_foto.clear()
        self.label_foto.setText("Iniciando cámara...")
        self.label_foto.setStyleSheet("color: gray; font-style: italic;")

        self.preview.start()

    def detener_camara(self):
        self.preview.stop()

    # ---------- captura y guardado ----------
    def capturar_foto(self) -> str | None:
        frame = self.preview.get_captured_frame()
        if frame is None:
            QMessageBox.warning(self.mw, "Captura", "No hay imagen para capturar.")
            return None

        #try:
            # rostro = self.detectar_y_recortar_rostro(frame)
            # if rostro is None:
            #     QMessageBox.warning(self.mw, "Captura", "No se detectó rostro.")
            #     return None

            # Recorte a proporción 4:5 centrado en rostro
            # final_img = self.recortar_a_proporcion(frame, rostro, proporcion=(4, 5), salida_px=(800, 1000))
            #
            # final_img = self.mejorar_imagen(final_img)
            #
            # ruta_foto = self.guardar_foto_temporal(final_img)
            # if not ruta_foto:
            #     return None

        try:
                # 👉 Solo recortar a 4:5 centrado sin detectar rostro
            final_img = self.recortar_frame_a_4_5(frame, salida_px=(800, 1000))
            final_img = self.mejorar_imagen(final_img)

            ruta_foto = self.guardar_foto_temporal(final_img)
            if not ruta_foto:
                return None

            self.ultima_ruta = str(ruta_foto)

            self.detener_camara()
            self.mostrar_en_label(final_img)  # Mostrar versión final recortada

            print(f"[CameraController] Foto final guardada en: {self.ultima_ruta}")
            return self.ultima_ruta

        except Exception as e:
            QMessageBox.critical(self.mw, "Error", f"Ocurrió un error al capturar la foto:\n{e}")
            return None



    def recortar_frame_a_4_5(self, frame, salida_px=(800, 1000)):
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

    def recortar_a_proporcion(self, frame, rostro, proporcion=(4, 5), salida_px=(800, 1000)):
        """
        Recorta una imagen con una proporción exacta centrada en el rostro detectado.
        - frame: imagen original
        - rostro: recorte del rostro para detectar coordenadas
        - proporcion: (ancho, alto) deseado
        - salida_px: resolución final
        """
        # Obtener tamaño original
        h_frame, w_frame = frame.shape[:2]

        # Coordenadas del rostro en la imagen original
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)

        if len(faces) == 0:
            return cv2.resize(frame, salida_px)

        x, y, w, h = faces[0]
        cx, cy = x + w // 2, y + h // 2  # Centro del rostro

        # Calcular tamaño del recorte con proporción 4:5
        aspect_w, aspect_h = proporcion
        target_ratio = aspect_w / aspect_h

        # Calcular alto basado en un ancho que contenga bien el rostro
        box_width = max(w, h * target_ratio) * 1.5
        box_height = box_width / target_ratio

        # Coordenadas finales asegurando que estén dentro de la imagen
        x1 = int(max(cx - box_width // 2, 0))
        y1 = int(max(cy - box_height // 2, 0))
        x2 = int(min(cx + box_width // 2, w_frame))
        y2 = int(min(cy + box_height // 2, h_frame))

        recorte = frame[y1:y2, x1:x2]

        return cv2.resize(recorte, salida_px, interpolation=cv2.INTER_AREA)

    def detectar_y_recortar_rostro(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]
        pad = int(0.4 * h)
        x1, y1 = max(x - pad, 0), max(y - pad, 0)
        x2, y2 = min(x + w + pad, frame.shape[1]), min(y + h + pad, frame.shape[0])

        rostro = frame[y1:y2, x1:x2]

        # Redimensionar al tamaño del QLabel
        size = self.label_foto.size()
        return cv2.resize(rostro, (size.width(), size.height()), interpolation=cv2.INTER_AREA)

    def mejorar_imagen(self, frame):
        return cv2.convertScaleAbs(frame, alpha=1.2, beta=20)

    def guardar_foto_temporal(self, frame) -> Path | None:
        ruta_foto = get_temp_foto_path()
        success = cv2.imwrite(str(ruta_foto), frame)
        if not success:
            QMessageBox.critical(self.mw, "Error", "No se pudo guardar la foto.")
            return None
        return ruta_foto

    def mostrar_en_label(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        qimg = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
        self.label_foto.setPixmap(QPixmap.fromImage(qimg))
        self.label_foto.setScaledContents(True)

    # ---------- getter ----------
    def get_ruta_foto(self) -> str | None:
        return self.ultima_ruta
