from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QRect, QSize, Signal, QEvent
from PySide6.QtGui import QIcon
from src.utils.rutas import get_icons_dir


def _get_icon_positions(option):
    # Tamaño de los íconos
    icon_size = QSize(20, 20)
    # Espacio entre íconos
    spacing = 10

    total_width = icon_size.width() * 2 + spacing
    start_x = option.rect.x() + (option.rect.width() - total_width) // 2
    y = option.rect.y() + (option.rect.height() - icon_size.height()) // 2

    editar_rect = QRect(start_x, y, icon_size.width(), icon_size.height())
    ver_rect = QRect(start_x + icon_size.width() + spacing, y, icon_size.width(), icon_size.height())

    return editar_rect, ver_rect


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
        editar_rect, ver_rect = _get_icon_positions(option)
        # Pintamos los íconos
        self.editar_icon.paint(painter, editar_rect)
        self.ver_icon.paint(painter, ver_rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            editar_rect, ver_rect = _get_icon_positions(option)
            mouse_pos = event.pos()

            if editar_rect.contains(mouse_pos):
                self.editarClicked.emit(index.row())
            elif ver_rect.contains(mouse_pos):
                self.verClicked.emit(index.row())
        return True
