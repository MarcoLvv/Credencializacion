from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtCore import QRect, QSize, Signal, QEvent
from PySide6.QtGui import QIcon
from src.utils.rutas import get_icons_path
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QBrush, QColor
from PySide6.QtCore import Qt

def _get_icon_positions(option):
    # Tamaño de los íconos
    icon_size = QSize(24, 24)
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
        edit_icon_path = get_icons_path("edit")
        view_icon_path = get_icons_path("view")
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

class CheckboxColorDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data(Qt.ItemDataRole.CheckStateRole)
        if value == Qt.CheckState.Checked:
            option.backgroundBrush = QBrush(QColor("#c8f7c5"))  # Verde
        elif value == Qt.CheckState.Unchecked:
            option.backgroundBrush = QBrush(QColor("#f7c5c5"))  # Rojo

        super().paint(painter, option, index)