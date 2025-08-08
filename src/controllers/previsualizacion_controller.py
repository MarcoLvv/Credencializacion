import os
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSizePolicy
from src.utils.rutas import get_background_back_side, get_background_front_side, get_layout_qr
from src.utils.helpers import (
    show_scaled_preview, CredencialRenderer,
)

class PreviewController:
    def __init__(self, ui, database):
        self.ui = ui
        self.db = database
        self.folio_id = ""
        self.front_image = None
        self.reverse_image = None
        self.temp_pdf_path = None
        self.render = CredencialRenderer(self.ui.frontWidgetCredential, self.ui.backWidgetCredential, self.ui)
        print("[DEBUG] PreviewController inicializado")
        self.ui.printBtn.clicked.connect(self.render.show_pdf_in_browser)

    def show_credential(self, data):
        # Cargar fondos y QR
        front_background = get_background_front_side("front_side")
        back_background = get_background_back_side("back_side")
        qr_path = get_layout_qr()

        show_scaled_preview(str(front_background), self.ui.labelFrontBackgroundCredential)
        show_scaled_preview(str(back_background), self.ui.labelReverseBackgroundCredential)
        show_scaled_preview(str(qr_path), self.ui.labelQrWhatsappCredential, scaled=True)

        # Ajustar etiquetas de texto
        for label in [self.ui.labelCredentialName, self.ui.labelCredentialAddress]:
            label.setWordWrap(True)
            label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        # Extraer datos del objeto o diccionario
        is_dict = isinstance(data, dict)
        get = data.get if is_dict else lambda k, default="": getattr(data, k, default)

        self.folio_id = get("FolioId", "")
        nombre_completo = " ".join(filter(None, [get("Nombre", ""), get("Paterno", ""), get("Materno", "")]))

        direccion = " ".join(filter(None, [
            f'{get("Calle", "")} #{get("NumExterior", "")}' if get("Calle", "") and get("NumExterior", "") else "",
            get("NumInterior", ""),
            f"MZ {get('Manzana', '')}" if get("Manzana", "") else "",
            f"LT {get('Lote', '')}" if get("Lote", "") else "",
            f"CP {get('CodigoPostal', '')}" if get("CodigoPostal", "") else "",
            get("Colonia", ""),
            get("Municipio", "")
        ]))

        self.ui.labelCredentialName.setText(nombre_completo)
        self.ui.labelCredentialAddress.setText(direccion)
        self.ui.labelCredentialCURP.setText(get("Curp", ""))
        self.ui.labelCredentialFolio.setText(self.folio_id)

        # Foto
        ruta_foto = get("RutaFoto", "")
        if ruta_foto and os.path.exists(ruta_foto):
            show_scaled_preview(ruta_foto, self.ui.labelUserPhotoCredencial)
        else:
            self.ui.labelUserPhotoCredencial.clear()
            self.ui.labelUserPhotoCredencial.setText("Sin foto")
            self.ui.labelUserPhotoCredencial.setStyleSheet("color: gray; font-style: italic;")

        # Firma
        ruta_firma = get("RutaFirma", "")
        if ruta_firma and os.path.exists(ruta_firma):
            show_scaled_preview(ruta_firma, self.ui.labelSignatureCredential)
        else:
            self.ui.labelSignatureCredential.clear()
            self.ui.labelSignatureCredential.setText("Sin firma")
            self.ui.labelSignatureCredential.setStyleSheet("color: gray; font-style: italic;")

        # Generar imágenes temporales y PDF
        self.render.generate_images_for_preview()


