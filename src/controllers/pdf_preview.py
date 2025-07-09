from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtPdf import QPdfDocument

class VistaPDF(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("vistaPDF")
        self.documento_pdf = QPdfDocument(self)
        self.vista = QPdfView()
        self.vista.setDocument(self.documento_pdf)

        self.btn_volver = QPushButton("Volver")


    def cargar_pdf(self, path_pdf):
        self.documento_pdf.load(path_pdf)
