import logging
import os

from PySide6.QtCore import Qt

from PySide6.QtWidgets import QSizePolicy
from src.utils.rutas import get_background_back_side, get_background_front_side, get_layout_qr
from src.utils.render_utils import (
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
        #print("[DEBUG] PreviewController inicializado")
        logging.debug("[DEBUG] PreviewController inicializado")
        self.ui.printBtn.clicked.connect(lambda: self.render.show_pdf_in_browser(self.db))

        # Conectar checkbox para cambiar background posterior
        self.ui.checkBoxBackgroundSignature.stateChanged.connect(self.toggle_signature_background)


    def show_credential(self, data):

        self.ui.checkBoxBackgroundSignature.setChecked(True)
        # Cargar fondos y QR
        front_background = get_background_front_side("front_side")
        back_background = get_background_back_side("back_side")
        qr_path = get_layout_qr()

        show_scaled_preview(str(front_background), self.ui.labelFrontBackgroundCredential, scaled=True)
        show_scaled_preview(str(back_background), self.ui.labelReverseBackgroundCredential, scaled=True)
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
        self.render.folio_id = self.folio_id  # donde folio es el ID o clave primaria de la credencial

        self.ui.labelCredentialName.setText(nombre_completo)
        self.ui.labelCredentialAddress.setText(direccion)
        self.ui.labelCredentialCURP.setText(get("CURP", ""))
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

        # Generar imágenes temporales y PDF
        self.render.generate_images_for_preview()

    def toggle_signature_background(self, state):
        """
        Cambia el fondo posterior entre versión con firma y sin firma.
        Soporta tanto int como enum en 'state'.
        """
        # Convertimos siempre a int para evitar problemas de comparación
        state_value = int(state) if not isinstance(state, int) else state

        logging.debug(f"[DEBUG] Estado checkbox recibido: {state} ({state_value})")

        if state_value == Qt.CheckState.Checked.value:  # 2
            logging.debug("[DEBUG] Checkbox activado → Fondo SIN firma")
            back_background = get_background_back_side("back_side")
        else:  # 0 o 1
            logging.debug("[DEBUG] Checkbox desactivado → Fondo CON firma")
            back_background = get_background_back_side("back_side_wo_signature")

        if back_background and back_background.exists():
            show_scaled_preview(str(back_background), self.ui.labelReverseBackgroundCredential, scaled=True)
            self.reverse_image = back_background
        else:
            logging.warning("[WARN] No se encontró el background posterior para la opción seleccionada")

