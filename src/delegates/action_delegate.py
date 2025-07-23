from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QRect, QSize, Signal, QEvent

from PySide6.QtGui import QIcon
from src.utils.rutas import get_icons_dir

class ActionDelegate(QStyledItemDelegate):
    editarClicked = Signal(int)
    verClicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        edit_icon_path = get_icons_dir() / "edit.png"
        view_icon_path = get_icons_dir() / "view.png"
        self.editar_icon = QIcon(str(edit_icon_path))  # ✔️ QIcon desde la ruta
        self.ver_icon = QIcon(str(view_icon_path))

    def paint(self, painter, option, index):
        icon_size = QSize(20, 20)  # Tamaño de los íconos
        spacing = 10  # Espacio entre íconos

        total_width = icon_size.width() * 2 + spacing
        start_x = option.rect.x() + (option.rect.width() - total_width) // 2
        y = option.rect.y() + (option.rect.height() - icon_size.height()) // 2

        editar_rect = QRect(start_x, y, icon_size.width(), icon_size.height())
        ver_rect = QRect(start_x + icon_size.width() + spacing, y, icon_size.width(), icon_size.height())

        self.editar_icon.paint(painter, editar_rect)
        self.ver_icon.paint(painter, ver_rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            icon_size = QSize(20, 20)
            spacing = 10

            total_width = icon_size.width() * 2 + spacing
            start_x = option.rect.x() + (option.rect.width() - total_width) // 2
            y = option.rect.y() + (option.rect.height() - icon_size.height()) // 2

            editar_rect = QRect(start_x, y, icon_size.width(), icon_size.height())
            ver_rect = QRect(start_x + icon_size.width() + spacing, y, icon_size.width(), icon_size.height())

            mouse_pos = event.pos()

            if editar_rect.contains(mouse_pos):
                self.editarClicked.emit(index.row())
            elif ver_rect.contains(mouse_pos):
                self.verClicked.emit(index.row())
        return True

