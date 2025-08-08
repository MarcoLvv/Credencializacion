from PySide6.QtCore import QObject, QSize
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon, Qt
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QPushButton

from src.utils.rutas import get_icons_path


# Funcion para colocar iconos.
def set_svg_icon(button: QPushButton, icon_name: str, size: QSize = None):
    svg_path = get_icons_path(icon_name)

    if not svg_path.exists():
        print(f"[WARNING] Icono no encontrado: {svg_path}")
        return

    renderer = QSvgRenderer(str(svg_path))
    pixmap = QPixmap(size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    # Crear pixmap blanco usando CompositionMode_SourceIn
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor('white'))
    painter.end()

    button.setIcon(QIcon(pixmap))
    button.setIconSize(size)

class set_svg_icons(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        #Iconos de los botones de la parte lateral izquierda

        set_svg_icon(self.ui.captureBtn, "capture.svg", QSize(24, 24))
        set_svg_icon(self.ui.homeBtn, "home.svg", QSize(24, 24))
        set_svg_icon(self.ui.importBtn, "database-import.svg", QSize(24, 24))
        set_svg_icon(self.ui.exportBtn, "database-export.svg", QSize(24, 24))

        #Iconos en La Vista de Captura
        set_svg_icon(self.ui.startPhotoBtn, "camera.svg", QSize(24, 24))

        set_svg_icon(self.ui.uploadPhotoBtn, "camera-search.svg", QSize(24, 24))
        set_svg_icon(self.ui.startSignatureBtn, "writing.svg", QSize(24, 24))
        set_svg_icon(self.ui.saveDataBtn, "folder-check.svg", QSize(24, 24))
