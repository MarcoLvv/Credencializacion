from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

from src.models.credencial_model import TbcUsuariosDAO


class UsuariosTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self.columns = [
            ("ID", "Id"),
            ("Folio", "FolioId"),
            ("Nombre", "Nombre"),
            ("Paterno", "Paterno"),
            ("Materno", "Materno"),
            ("Sección Electoral", "SeccionElectoral"),
            ("Acciones", None),
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        column = index.column()
        if row >= len(self._data):
            return None

        _, attr = self.columns[column]
        usuario = self._data[row]

        if role == Qt.ItemDataRole.DisplayRole:
            if attr is None:
                return ""
            valor = getattr(usuario, attr, "")
            return str(valor) if valor is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if attr is None:
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self.columns[section][0]
        elif orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsSelectable or Qt.ItemFlag.ItemIsEnabled

    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data or []
        self.endResetModel()

    def get_row_data(self, row):
        if 0 <= row < len(self._data):
            return self._data[row]
        return None

    def update_row(self, row):
        if 0 <= row < len(self._data):
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])

    def sort(self, column, order):
        attr = self.columns[column][1]
        if attr is None:
            return
        self.layoutAboutToBeChanged.emit()
        self._data.sort(
            key=lambda x: str(getattr(x, attr, "") or ""),
            reverse=(order == Qt.SortOrder.DescendingOrder),
        )
        self.layoutChanged.emit()

    def get_all_data(self):
        return self._data
