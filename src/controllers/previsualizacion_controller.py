import os
import shutil
import tempfile
import webbrowser
from pathlib import Path

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox, QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView

from src.integrations.impresora_zebra import generar_pdf_doble_cara
from src.utils.rutas import get_layout_front, get_layout_back, get_layout_QR, get_temp_credencial_paths, get_foto_dir


class PrevisualizacionController:
    def __init__(self, ui):
        self.ui = ui
        self.imagen_frontal = None
        self.imagen_reverso = None
        self.web_view: QWebEngineView = self.ui.webPreview  # Asumiendo que ya está creado desde QtDesigner
        self.ruta_pdf_temporal = None

        self.ui.btnImprimir.clicked.connect(self.imprimir_credencial)

    def mostrar_credencial(self, data):
        # Cargar imágenes de fondo
        fondo_path = get_layout_front()
        fondo_path_posterior = get_layout_back()
        fondo_path_qr = get_layout_QR()

        self.ui.labelFondo.setPixmap(QPixmap(str(fondo_path)))
        self.ui.labelFondo.setScaledContents(True)
        self.ui.labelFondoPosterior.setPixmap(QPixmap(str(fondo_path_posterior)))
        self.ui.labelFondoPosterior.setScaledContents(True)
        self.ui.labelQrWhatsapp.setPixmap(QPixmap(str(fondo_path_qr)))
        self.ui.labelQrWhatsapp.setScaledContents(True)

        # Habilita el ajuste automático del texto
        self.ui.labelNombreCredencial.setWordWrap(True)

        # Si estás usando layouts, asegúrate que el layout permita crecimiento vertical
        self.ui.labelNombreCredencial.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Maximum
        )

        # Habilita el ajuste automático del texto
        self.ui.labelDomicilioCredencial.setWordWrap(True)
        
        # Si estás usando layouts, asegúrate que el layout permita crecimiento vertical
        self.ui.labelDomicilioCredencial.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Maximum
        )
        if isinstance(data, dict):
            folio = data.get("FolioId", "")
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
            folio = data.FolioId
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

        nombre_completo = f"{nombre} {paterno} {materno}"

        self.ui.labelNombreCredencial.setText(nombre_completo)

        Domicilio = f"""{calle} #{numExterior} {numInterior} {manzana} {codigoPostal} {colonia} {municipio}"""
        self.ui.labelDomicilioCredencial.setText(Domicilio)

        self.ui.labelCURPCredencial.setText(curp)
        self.ui.labelFolioCredencial.setText(folio)

        if ruta_foto and os.path.exists(ruta_foto):
            self.ui.labelFotoCredencial.setPixmap(QPixmap(ruta_foto))
            self.ui.labelFotoCredencial.setScaledContents(True)

        if ruta_firma and os.path.exists(ruta_firma):
            self.ui.labelFirmaCredencial.setPixmap(QPixmap(ruta_firma))
            self.ui.labelFirmaCredencial.setScaledContents(True)

        # Generar imágenes temporales
        self.generar_imagenes_credencial()
        # Generar y mostrar PDF en webPreview
        self.mostrar_pdf_en_webview()
        #Mostrar imagenes en navegador externo

        self.mostrar_pdf_externo()

    def mostrar_pdf_externo(self):
        if self.ruta_pdf_temporal:
            webbrowser.open(self.ruta_pdf_temporal)

    def ver_desde_credencial(self, credencial):
        data = {
            "Nombre": credencial.Nombre,
            "Paterno": credencial.Paterno,
            "Materno": credencial.Materno,
            "ruta_foto": credencial.RutaFoto,
            "ruta_firma": credencial.RutaFirma,
        }
        self.mostrar_credencial(data)

    def generar_imagenes_credencial(self):
        try:
            self.limpiar_temporales()  # Borra archivos antiguos si aplica

            ruta_frontal, ruta_posterior = get_temp_credencial_paths()

            # Captura los pixmaps de los frames
            pixmap_frontal = self.ui.frameFrontal.grab()
            pixmap_posterior = self.ui.framePosterior.grab()

            # Guardar archivos
            if not pixmap_frontal.save(str(ruta_frontal)):
                raise Exception("No se pudo guardar imagen frontal.")
            if not pixmap_posterior.save(str(ruta_posterior)):
                raise Exception("No se pudo guardar imagen posterior.")

            print(f"[OK] Imagen temporal frontal: {ruta_frontal}")
            print(f"[OK] Imagen temporal posterior: {ruta_posterior}")

            self.set_imagenes_credencial(str(ruta_frontal), str(ruta_posterior))

        except Exception as e:
            print(f"[ERROR] No se pudo generar imagen temporal de la credencial: {e}")
            QMessageBox.critical(self.ui, "Error", f"No se pudo generar la credencial:\n{e}")

    def guardar_credencial_final(self, persona_id: str):
        base_dir = get_foto_dir() / "credenciales"
        base_dir.mkdir(parents=True, exist_ok=True)

        frontal_final = base_dir / f"{persona_id}_frontal.png"
        posterior_final = base_dir / f"{persona_id}_posterior.png"

        ruta_frontal, ruta_posterior = get_temp_credencial_paths()

        shutil.copy(ruta_frontal, frontal_final)
        shutil.copy(ruta_posterior, posterior_final)

        print(f"[✔] Credencial guardada en:\n - {frontal_final}\n - {posterior_final}")

    def mostrar_pdf_en_webview(self):
        try:
            if not self.imagen_frontal or not self.imagen_reverso:
                raise Exception("No hay imágenes para generar el PDF.")

            pdf_path = generar_pdf_doble_cara(self.imagen_frontal, self.imagen_reverso)
            self.ruta_pdf_temporal = Path(pdf_path).resolve().as_uri()

            print(f"[OK] PDF generado correctamente en: {pdf_path}")
            print(f"[OK] Intentando cargar PDF en visor Web: {self.ruta_pdf_temporal}")

            self.web_view.load(str(self.ruta_pdf_temporal))

            self.ui.stackedWidget.setCurrentWidget(self.ui.pagePDF)

        except Exception as e:
            print(f"[ERROR] No se pudo mostrar el PDF: {e}")
            QMessageBox.critical(None, "Error", f"No se pudo mostrar el PDF: {e}")

    def imprimir_credencial(self):
        try:
            if not self.imagen_frontal or not self.imagen_reverso:
                raise Exception("No hay imágenes listas para imprimir.")
            generar_pdf_doble_cara(self.imagen_frontal, self.imagen_reverso)
            QMessageBox.information(None, "Impresión", "Trabajo enviado a Zebra ZC300.")
        except Exception as e:
            QMessageBox.critical(None, "Error de impresión", str(e))

    def set_imagenes_credencial(self, frontal_path, reverso_path):
        self.imagen_frontal = frontal_path
        self.imagen_reverso = reverso_path

    def limpiar_temporales(self):
        temp_dir = Path(tempfile.gettempdir()) / "credenciales_temp"
        for archivo in ["credencial_frontal.png", "credencial_reverso.png"]:
            ruta = temp_dir / archivo
            if ruta.exists():
                try:
                    ruta.unlink()
                    print(f"[INFO] Archivo temporal eliminado: {ruta}")
                except Exception as e:
                    print(f"[WARN] No se pudo eliminar {ruta}: {e}")
