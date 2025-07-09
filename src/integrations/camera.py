import cv2
from PySide6.QtWidgets import (
	QMainWindow, QLabel,QComboBox,
	QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap


class CameraPreview:
	def __init__(self, target_label, camera_index=1):
		self.label = target_label
		self.cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)  # Importante en Windows
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_frame)
		self.frame_actual = None
		self.camera_index = camera_index

	def start(self):
		# Si ya hay una cámara abierta, liberarla primero
		if self.cap.isOpened():
			self.cap.release()

		# Reabrir cámara con el índice original
		self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)

		if self.cap.isOpened():
			# Establecer resolución máxima posible (intenta Full HD)
			self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
			self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

			self.timer.start(30)
			print("[CameraPreview] Cámara iniciada correctamente.")
		else:
			print("[ERROR] No se pudo abrir la cámara.")

	def stop(self):
		self.timer.stop()
		if self.cap.isOpened():
			self.cap.release()
	
	def update_frame(self):
		ret, frame = self.cap.read()
		if not ret:
			return
		
		target_size = self.label.size()
		resized_frame = cv2.resize(frame, (target_size.width(), target_size.height()))
		self.frame_actual = resized_frame.copy()
		
		# Dibujar cruz guía
		h, w, _ = resized_frame.shape
		cv2.line(resized_frame, (w // 2, 0), (w // 2, h), (0, 255, 0), 1)
		cv2.line(resized_frame, (0, h // 2), (w, h // 2), (0, 255, 0), 1)
		
		# Convertir a QImage
		rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
		qimg = QImage(rgb_frame.data, w, h, w * 3, QImage.Format.Format_RGB888)
		pixmap = QPixmap.fromImage(qimg)
		scaled_pixmap = pixmap.scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
		self.label.setPixmap(scaled_pixmap)
	
	def get_captured_frame(self):
		return self.frame_actual.copy() if self.frame_actual is not None else None


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Selector de Cámara")
		
		# Crear widgets
		self.label_video = QLabel("Vista previa de cámara")
		self.label_video.setFixedSize(640, 480)
		self.combo_camaras = QComboBox()
		self.btn_iniciar = QPushButton("Iniciar cámara")
		
		# Layout
		layout = QVBoxLayout()
		layout.addWidget(self.combo_camaras)
		layout.addWidget(self.btn_iniciar)
		layout.addWidget(self.label_video)
		
		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)
		
		# Lógica
		self.camera_preview = None
		self.detectar_camaras()
		
		self.btn_iniciar.clicked.connect(self.iniciar_camara)
	
	def detectar_camaras(self):
		for i in range(5):
			cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
			if cap.isOpened():
				self.combo_camaras.addItem(f"Cámara {i}", i)
				cap.release()
	
	def iniciar_camara(self):
		index = self.combo_camaras.currentData()
		if self.camera_preview:
			self.camera_preview.stop()
		self.camera_preview = CameraPreview(self.label_video, index)
		self.camera_preview.start()



