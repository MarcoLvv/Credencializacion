import comtypes.client
from pathlib import Path
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox
from src.database.db_manager import DBManager
from PIL import Image

from src.utils.rutas import get_firma_dir, get_temp_firma_path


class FirmaController:
    def __init__(self, parent_window=None, label_firma=None):
        self.parent_window = parent_window
        self.ui = parent_window
        self.label_firma = label_firma  # QLabel donde se mostrará la firma

        self.db = DBManager()
        self.firma_dir = get_firma_dir()
        self.ruta_firma_actual = None

        # Estado: 0 = Iniciar cámara, 1 = Capturar, 2 = Repetir
        self.estado = 0
        self.botones_texto = ["Iniciar Firma", "Capturar", "Repetir"]


        self.sigCtl = comtypes.client.CreateObject("SIGPLUS.SigPlusCtrl.1")
        self.sigCtl.InitSigPlus()
        self.sigCtl.SetImageScreenResolution(300)

    def manejar_estado_firma(self):
        if self.estado == 0:
            self.iniciar_capturar_firma()
        elif self.estado == 1:
            self.capturar_firma()
        elif self.estado == 2:
            self.iniciar_capturar_firma()  # Repetir vuelve a iniciar cámara

        # Cambiar al siguiente estado (cíclico)
        self.estado = (self.estado + 1) % 3
        self.ui.btnIniciarFirma.setText(self.botones_texto[self.estado])


    def iniciar_capturar_firma(self):
        # Limpia el QLabel de la firma si ya había algo mostrado
        if self.label_firma:
            self.label_firma.clear()
            self.label_firma.setText("Esperando firma...")
            self.label_firma.setStyleSheet("color: gray; font-style: italic;")

        self.sigCtl.ClearTablet()
        self.sigCtl.SetSigWindow(1, 0, 0, 500, 200)

        self.sigCtl.EnableTabletCapture()
        self.sigCtl.TabletConnectQuery()

        print("[SignaturePad] Captura iniciada. Esperando firma...")


    def capturar_firma(self) -> str | None:
        puntos = self.sigCtl.NumberOfTabletPoints()
        print(f"[SignaturePad] Puntos capturados: {puntos}")

        if puntos == 0:
            QMessageBox.warning(self.parent_window, "Firma", "No se detectó firma.")
            return None

        try:
            ruta_firma_temp = self.guardar_firma_temporal()
            if not ruta_firma_temp:
                return None

            self.ruta_firma_actual = str(ruta_firma_temp)

            self.mostrar_firma_en_label(self.ruta_firma_actual)
            self.limpiar_firma()

            return self.ruta_firma_actual

        except Exception as e:
            QMessageBox.critical(self.parent_window, "Error al guardar firma", str(e))
            return None

    def guardar_firma_temporal(self) -> Path | None:
        ruta_firma = get_temp_firma_path()
        self.sigCtl.ImagePenWidth = 15

        guardado = self.sigCtl.WriteImageFile(str(ruta_firma))
        if not guardado:
            QMessageBox.critical(self.parent_window, "Error", "No se pudo guardar la imagen.")
            return None

        self.convertir_fondo_transparente(ruta_firma)
        print(f"[FirmaController] Firma temporal guardada en: {ruta_firma}")
        return ruta_firma

    def mostrar_firma_en_label(self, ruta_img: str):
        if self.label_firma:
            pixmap = QPixmap(ruta_img)
            self.label_firma.setPixmap(pixmap)
            self.label_firma.setScaledContents(True)

    def limpiar_firma(self):
        self.sigCtl.DisableTabletCapture()
        self.sigCtl.ClearTablet()

    def convertir_fondo_transparente(self, ruta_firma: Path):
        try:
            # Abrir la imagen con PIL
            image = Image.open(ruta_firma)

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
            image.save(ruta_firma, "PNG")
            print(f"[FirmaController] Imagen convertida a transparente: {ruta_firma}")

        except Exception as e:
            QMessageBox.critical(self.parent_window, "Error al procesar la firma", f"Error: {str(e)}")

    def get_ruta_firma(self) -> str | None:
        return self.ruta_firma_actual
