import comtypes.client
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from src.database.db_manager import DBManager
from PIL import Image

from src.utils.rutas import get_firma_dir, get_temp_firma_path


class SignatureController:
    def __init__(self, parent_window=None, signature_label=None):
        self.parent_window = parent_window
        self.ui = parent_window
        self.signature_label = signature_label  # QLabel donde se mostrará la firma

        self.db = DBManager()
        self.signature_path = get_firma_dir()
        self.current_signature_path = None

        # Estado: 0 = Iniciar cámara, 1 = Capturar, 2 = Repetir
        self.status = 0
        self.text_buttons = ["Iniciar Firma", "Capturar", "Repetir"]


        self.sigCtl = comtypes.client.CreateObject("SIGPLUS.SigPlusCtrl.1")
        self.sigCtl.InitSigPlus()
        self.sigCtl.SetImageScreenResolution(300)

    def manage_signature_state(self):
        if self.status == 0:
            self.start_capture_signature()
        elif self.status == 1:
            self.capture_signature()
        elif self.status == 2:
            self.start_capture_signature()  # Repetir vuelve a iniciar cámara

        # Cambiar al siguiente estado (cíclico)
        self.status = (self.status + 1) % 3
        self.ui.btnStartSignature.setText(self.text_buttons[self.status])


    def start_capture_signature(self):
        # Limpia el QLabel de la firma si ya había algo mostrado
        if self.signature_label:
            self.signature_label.clear()
            self.signature_label.setText("Esperando firma...")
            self.signature_label.setStyleSheet("color: gray; font-style: italic;")

        self.sigCtl.ClearTablet()
        self.sigCtl.SetSigWindow(1, 0, 0, 500, 200)

        self.sigCtl.EnableTabletCapture()
        self.sigCtl.TabletConnectQuery()

        #print("[SignaturePad] Captura iniciada. Esperando firma...")


    def capture_signature(self) -> str | None:
        points = self.sigCtl.NumberOfTabletPoints()
        #print(f"[SignaturePad] Puntos capturados: {points}")

        if points == 0:
            QMessageBox.warning(self.parent_window, "Firma", "No se detectó firma.")
            return None

        try:
            signature_path_temp = self.save_temporary_signature()
            if not signature_path_temp:
                return None

            self.current_signature_path = str(signature_path_temp)

            self.show_signature_label(self.current_signature_path)
            self.clean_signature()

            return self.current_signature_path

        except Exception as e:
            QMessageBox.critical(self.parent_window, "Error al guardar firma", str(e))
            return None

    def save_temporary_signature(self) -> Path | None:
        temp_signature_path = get_temp_firma_path()
        self.sigCtl.ImagePenWidth = 15

        save_signature = self.sigCtl.WriteImageFile(str(temp_signature_path))
        if not save_signature:
            QMessageBox.critical(self.parent_window, "Error", "No se pudo guardar la imagen.")
            return None

        self.convert_transparent_background(temp_signature_path)
        print(f"[FirmaController] Firma temporal guardada en: {temp_signature_path}")
        return temp_signature_path

    def show_signature_label(self, ruta_img: str):
        if self.signature_label:
            pixmap = QPixmap(ruta_img)
            self.signature_label.setPixmap(pixmap)
            self.signature_label.setScaledContents(True)

    def clean_signature(self):
        self.sigCtl.DisableTabletCapture()
        self.sigCtl.ClearTablet()

    def convert_transparent_background(self, temp_signature_path: Path):
        try:
            # Abrir la imagen con PIL
            image = Image.open(temp_signature_path)

            # Convertir la imagen a RGBA para incluir el canal alpha (transparencia)
            image = image.convert("RGBA")

            # Obtener los datos de los píxeles
            datas = image.getdata()

            new_data = []
            for item in datas:
                # Si el píxel es blanco (o muy cercano a blanco), hacerlo transparente
                if item[0] in list(range(200, 256)) and item[1] in list(range(200, 256)) and item[2] in list(range(200, 256)):
                    new_data.append((255, 255, 255, 0))  # Fondo transparente
                else:
                    new_data.append(item)

            # Reemplazar los datos de los píxeles en la imagen
            image.putdata(new_data)

            # Guardar la imagen como PNG con transparencia
            image.save(temp_signature_path, "PNG")
            print(f"[FirmaController] Imagen convertida a transparente: {temp_signature_path}")

        except Exception as e:
            QMessageBox.critical(self.parent_window, "Error al procesar la firma", f"Error: {str(e)}")

    def get_temp_signature_path(self) -> str | None:
        return self.current_signature_path
