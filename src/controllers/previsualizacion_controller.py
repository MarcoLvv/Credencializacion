import os
import shutil
import tempfile
import webbrowser
from pathlib import Path

from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QMessageBox, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView

from src.utils.pdf_utils import generar_pdf_doble_cara
from src.utils.rutas import get_background_front_side, get_background_back_side, get_layout_qr, get_temp_credencial_sides_paths, get_foto_dir


class PreviewController:
    def __init__(self, ui):
        print("[DEBUG] PrevisualizacionController inicializado")
        self.ui = ui
        self.front_image = None
        self.reverse_image = None
        self.temp_pdf_path = None

        self.ui.printBtn.clicked.connect(self.show_pdf_browser)

    def show_credential(self, data):

        # Cargar imágenes de fondo
        front_background_path = get_background_front_side()
        reverse_background_path = get_background_back_side()
        whatsapp_famc_qr_path = get_layout_qr()

        self.ui.labelFrontBackgroundCredential.setPixmap(QPixmap(str(front_background_path)))
        self.ui.labelFrontBackgroundCredential.setScaledContents(True)
        self.ui.labelReverseBackgroundCredential.setPixmap(QPixmap(str(reverse_background_path)))
        self.ui.labelReverseBackgroundCredential.setScaledContents(True)
        self.ui.labelQrWhatsappCredential.setPixmap(QPixmap(str(whatsapp_famc_qr_path)))
        self.ui.labelQrWhatsappCredential.setScaledContents(True)

        # Habilita el ajuste automático del texto
        self.ui.labelCredentialName.setWordWrap(True)

        # Si estás usando layouts, asegúrate que el layout permita crecimiento vertical
        self.ui.labelCredentialName.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Maximum
        )

        # Habilita el ajuste automático del texto
        self.ui.labelCredentialAddress.setWordWrap(True)

        # Si estás usando layouts, asegúrate que el layout permita crecimiento vertical
        self.ui.labelCredentialAddress.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Maximum
        )
        if isinstance(data, dict):
            folio_id = data.get("FolioId", "")
            nombre = data.get("Nombre", "")
            paterno = data.get("Paterno", "")
            materno = data.get("Materno", "")
            curp = data.get("Curp", "")
            calle = data.get("Calle", "")
            numExterior = data.get("NumExterior", "")
            numInterior = data.get("NumInterior", "")
            manzana = data.get("Manzana", "")
            lote = data.get("Lote", "")
            colonia = data.get("Colonia", "")
            codigoPostal = data.get("CodigoPostal", "")
            municipio = data.get("Municipio", "")
            ruta_foto = data.get("RutaFoto", "")
            ruta_firma = data.get("RutaFima", "")
        else:
            folio_id = data.FolioId
            nombre = data.Nombre
            paterno = data.Paterno
            materno = data.Materno
            curp = data.CURP
            calle = data.Calle
            numExterior = data.NumExterior
            numInterior = data.NumInterior
            manzana = data.Manzana
            lote = data.Lote
            colonia = data.Colonia
            codigoPostal = data.CodigoPostal
            municipio = data.Municipio
            ruta_foto = data.RutaFoto
            ruta_firma = data.RutaFirma

        complete_name = f"{nombre} {paterno} {materno}"

        self.ui.labelCredentialName.setText(complete_name)

        address = f"""{calle} #{numExterior} {numInterior} {manzana} {codigoPostal} {colonia} {municipio}"""
        self.ui.labelCredentialAddress.setText(address)

        self.ui.labelCredentialCURP.setText(curp)
        self.ui.labelCredentialFolio.setText(folio_id)

        # Limpia imágenes anteriores
        self.ui.labelUserPhotoCredencial.clear()
        self.ui.labelSignatureCredential.clear()

        # Foto de usuario
        if ruta_foto and os.path.exists(ruta_foto):
            pixmap = QPixmap(ruta_foto)
            self.ui.labelUserPhotoCredencial.setPixmap(pixmap.scaled(
            self.ui.labelUserPhotoCredencial.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
            #self.ui.labelUserPhotoCredencial.setFixedSize(200, 250)
        else:
            self.ui.labelUserPhotoCredencial.setText("Sin foto")
            self.ui.labelUserPhotoCredencial.setStyleSheet("color: gray; font-style: italic;")

        # Firma del usuario
        if ruta_firma and os.path.exists(ruta_firma):
            self.ui.labelSignatureCredential.setPixmap(QPixmap(ruta_firma))
            self.ui.labelSignatureCredential.setScaledContents(True)
        else:
            self.ui.labelSignatureCredential.setText("Sin firma")
            self.ui.labelSignatureCredential.setStyleSheet("color: gray; font-style: italic;")

        # Generar imágenes temporales
        self.generate_images_for_credentials()
        # Generar y mostrar PDF en webPreview
        #self.mostrar_pdf_en_webview()
        #Mostrar imagenes en navegador externo

        #self.mostrar_pdf_externo()

    def show_pdf_browser(self):
        pdf_path = generar_pdf_doble_cara(self.front_image, self.reverse_image)
        self.temp_pdf_path = Path(pdf_path).resolve().as_uri()
        if self.temp_pdf_path:
            webbrowser.open(self.temp_pdf_path)

    def view_from_credential(self, credencial):
        data = {
            "Nombre": credencial.Nombre,
            "Paterno": credencial.Paterno,
            "Materno": credencial.Materno,
            "ruta_foto": credencial.RutaFoto,
            "ruta_firma": credencial.RutaFirma,
        }
        self.show_credential(data)

    def generate_images_for_credentials(self):
        try:
            self.clean_temp()  # Borra archivos antiguos si aplica

            front_path, reverse_path = get_temp_credencial_sides_paths()

            # Captura los pixmaps de los frames
            front_pixmap = self.ui.frontFrameCredential.grab()
            back_pixmap = self.ui.backFrameCredential.grab()

            # Guardar archivos
            if not front_pixmap.save(str(front_path)):
                raise Exception("No se pudo guardar imagen frontal.")
            if not back_pixmap.save(str(reverse_path)):
                raise Exception("No se pudo guardar imagen posterior.")

            print(f"[OK] Imagen temporal frontal: {front_path}")
            print(f"[OK] Imagen temporal posterior: {reverse_path}")

            self.set_credential_images(str(front_path), str(reverse_path))

        except Exception as e:
            print(f"[ERROR] No se pudo generar imagen temporal de la credencial: {e}")
            QMessageBox.critical(self.ui.homeView, "Error", f"No se pudo generar la credencial:\n{e}")

    def save_final_credential(self, persona_id: str):
        base_dir = get_foto_dir() / "credenciales"
        base_dir.mkdir(parents=True, exist_ok=True)

        finished_front = base_dir / f"{persona_id}_frontal.png"
        finished_back = base_dir / f"{persona_id}_posterior.png"

        front_path, reverse_path = get_temp_credencial_sides_paths()

        shutil.copy(front_path, finished_front)
        shutil.copy(reverse_path, finished_back)

        print(f"[✔] Credencial guardada en:\n - {finished_front}\n - {finished_back}")

    def mostrar_pdf_en_webview(self):
        print("[DEBUG] mostrar_pdf_en_webview llamado")
        try:
            # if not self.front_image or not self.reverse_image:
            #     raise Exception("No hay imágenes para generar el PDF.")

            pdf_path = generar_pdf_doble_cara(self.front_image, self.reverse_image)
            self.temp_pdf_path = Path(pdf_path).resolve().as_uri()

            print(f"[OK] PDF generado correctamente en: {pdf_path}")
            print(f"[OK] Intentando cargar PDF en visor Web: {self.temp_pdf_path}")

            if self.temp_pdf_path:
                webbrowser.open(self.temp_pdf_path)


        except Exception as e:
            print(f"[ERROR] No se pudo mostrar el PDF: {e}")
            QMessageBox.critical(None, "Error", f"No se pudo mostrar el PDF: {e}")

    # def imprimir_credencial(self):
    #     try:
    #         if not self.front_image or not self.reverse_image:
    #             raise Exception("No hay imágenes listas para imprimir.")
    #         generar_pdf_doble_cara(self.front_image, self.reverse_image)
    #         QMessageBox.information(None, "Impresión", "Trabajo enviado a Zebra ZC300.")
    #     except Exception as e:
    #         QMessageBox.critical(None, "Error de impresión", str(e))

    def set_credential_images(self, frontal_path, reverso_path):
        self.front_image = frontal_path
        self.reverse_image = reverso_path

    def clean_temp(self):

        # Revisar donde se guardan para ver que no interfiera con alguna funcion
        temp_credential_path = Path(tempfile.gettempdir()) / "credenciales_temp"
        for credential_side in ["credencial_frontal.png", "credencial_reverso.png"]:
            temp_credential_side = temp_credential_path / credential_side
            if temp_credential_side.exists():
                try:
                    temp_credential_side.unlink()
                    print(f"[INFO] Archivo temporal eliminado: {temp_credential_side}")
                except Exception as e:
                    print(f"[WARN] No se pudo eliminar {temp_credential_side}: {e}")
