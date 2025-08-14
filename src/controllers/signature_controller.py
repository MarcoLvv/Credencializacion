import logging
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from PIL import Image
import comtypes.client

from src.database.db_manager import DBManager
from src.utils.rutas import get_firma_dir, get_temp_firma_path

class SignatureController:
    def __init__(self, parent_window=None, signature_label=None):
        self.parent_window = parent_window
        self.signature_label = signature_label
        self.ui = parent_window
        self.db = DBManager()

        logging.debug("[Signature] Inicializando dispositivo de firma")
        print("[Signature] Inicializando dispositivo de firma")

        self.sigCtl = comtypes.client.CreateObject("SIGPLUS.SigPlusCtrl.1")
        self.sigCtl.InitSigPlus()
        self.sigCtl.SetImageScreenResolution(300)

        self.signature_path = get_firma_dir()
        self.last_signature_path = ""
        self.status = 0  # 0: iniciar, 1: capturar, 2: repetir

    def manage_signature_state(self):
        logging.debug(f"[Signature] Estado actual: {self.status}")
        print(f"[Signature] Estado actual: {self.status}")
        actions = {
            0: self.prepare_signature_state,
            1: self.capture_signature,
            2: self.repeat_signature
        }
        actions.get(self.status, lambda: print("[Signature] Acción no definida"))()

    def prepare_signature_state(self):
        logging.debug("[Signature] Preparando estado de firma")
        self.clear_label()
        self._set_label_text("Esperando Firma", italic=True)
        self.last_signature_path = ""
        self._update_button("Capturar Firma", True)
        self._start_capture()
        self.status = 1

    def capture_signature(self):
        logging.debug("[Signature] Intentando capturar firma")
        print("[Signature] Verificando puntos capturados...")

        points = self.sigCtl.NumberOfTabletPoints()
        print(f"[Signature] Puntos capturados: {points}")
        logging.debug(f"[Signature] Puntos capturados: {points}")

        if points == 0:
            QMessageBox.warning(self.parent_window.captureView, "Firma", "No se detectó firma.")
            return None

        try:
            signature_path = self._save_signature()
            if not signature_path:
                return None

            self.last_signature_path = str(signature_path)
            self._show_signature(self.last_signature_path)
            self._clean_device()
            self._update_button("Repetir Firma")
            self.status = 2

            return self.last_signature_path

        except Exception as e:
            logging.exception("[Signature] Error al guardar la firma")
            QMessageBox.critical(self.parent_window, "Error al guardar firma", str(e))
            return None

    def repeat_signature(self):
        logging.debug("[Signature] Repetir firma")
        self.last_signature_path = ""
        self.prepare_signature_state()

    def _start_capture(self):
        logging.debug("[Signature] Iniciando captura en tableta")
        self.sigCtl.ClearTablet()
        self.sigCtl.SetSigWindow(1, 0, 0, 500, 200)
        self.sigCtl.EnableTabletCapture()
        connected = self.sigCtl.TabletConnectQuery()
        print(f"[Signature] Tableta conectada: {connected}")
        logging.debug(f"[Signature] Tableta conectada: {connected}")

    def _save_signature(self) -> Path | None:
        temp_path = get_temp_firma_path()
        self.sigCtl.ImagePenWidth = 15

        saved = self.sigCtl.WriteImageFile(str(temp_path))
        print(f"[Signature] Resultado de guardar imagen: {saved}")
        if not saved:
            QMessageBox.critical(self.parent_window, "Error", "No se pudo guardar la imagen.")
            return None

        self._make_background_transparent(temp_path)
        logging.debug(f"[Signature] Firma guardada en: {temp_path}")
        return temp_path

    def _make_background_transparent(self, image_path: Path):
        try:
            img = Image.open(image_path).convert("RGBA")
            new_data = [
                (255, 255, 255, 0) if all(c >= 200 for c in item[:3]) else item
                for item in img.getdata()
            ]
            img.putdata(new_data)
            img.save(image_path, "PNG")
            print(f"[Signature] Fondo transparente aplicado: {image_path}")
        except Exception as e:
            logging.exception("[Signature] Error al procesar fondo transparente")
            QMessageBox.critical(self.parent_window, "Error al procesar la firma", str(e))

    def _show_signature(self, image_path: str):
        if self.signature_label:
            print(f"[Signature] Mostrando firma: {image_path}")
            pixmap = QPixmap(image_path)
            self.signature_label.setPixmap(pixmap)
            self.signature_label.setScaledContents(True)

    def _clean_device(self):
        logging.debug("[Signature] Limpiando dispositivo de firma")
        self.sigCtl.DisableTabletCapture()
        self.sigCtl.ClearTablet()

    def _update_button(self, text, enabled=True):
        if self.parent_window and hasattr(self.parent_window, "startSignatureBtn"):
            print(f"[Signature] Actualizando botón: {text} - Enabled: {enabled}")
            self.parent_window.startSignatureBtn.setText(text)
            self.parent_window.startSignatureBtn.setEnabled(enabled)

    def _set_label_text(self, text, italic=False):
        if self.signature_label:
            style = "color: gray;"
            if italic:
                style += " font-style: italic;"
            self.signature_label.setText(text)
            self.signature_label.setStyleSheet(style)

    def clear_label(self):
        if self.signature_label:
            self.signature_label.clear()

    def get_temp_signature_path(self) -> str | None:
        return self.last_signature_path
