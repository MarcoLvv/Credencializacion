import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap


class CameraPreview:
    def __init__(self, target_label):
        self.label = target_label
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_frame)
        self.current_frame = None

    def start(self):
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("No se pudo abrir la cámara.")
            return
        self.timer.start(30)

    def stop(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None
        self.label.clear()
        self.current_frame = None

    def _update_frame(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        self.current_frame = frame
        self._mostrar_en_label(frame)

    def _mostrar_en_label(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = rgb.shape[:2]
        qimg = QImage(rgb.data, w, h, rgb.strides[0], QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qimg))
        self.label.setScaledContents(True)

    def get_captured_frame(self):
        return self.current_frame.copy() if self.current_frame is not None else None
