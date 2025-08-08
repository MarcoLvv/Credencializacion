from PySide6.QtCore import QObject, QSize

from src.utils.helpers import set_svg_icon


class set_svg_icons(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.ui = main_window
        set_svg_icon(self.ui.startPhotoBtn, "camera.svg", QSize(24, 24))
        set_svg_icon(self.ui.startSignatureBtn, "writing.svg", QSize(24, 24))