from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex



class UsuariosTableModel(QAbstractTableModel):
    def __init__(self, data=None , model_dao = None):
        super().__init__()
        self._data = data or []
        self.dao = model_dao
        self.columns = [
            ("ID", "Id"),
            ("Folio", "FolioId"),
            ("Nombre", "Nombre"),
            ("Paterno", "Paterno"),
            ("Materno", "Materno"),
            ("Sección Electoral", "SeccionElectoral"),
            ("Acciones", None),
            #("Entregada", "Entregada"),  # ✅ NUEVA COLUMNA CON CHECKBOX
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
        _, attr = self.columns[column]
        usuario = self._data[row]

        if role == Qt.ItemDataRole.CheckStateRole and attr == "Entregada":
            value = getattr(usuario, attr, False)
            return Qt.CheckState.Checked if value else Qt.CheckState.Unchecked

        if role == Qt.ItemDataRole.DisplayRole:
            if attr is None or attr == "Entregada":
                return ""  # Evita que muestre "False"
            return str(getattr(usuario, attr, ""))


        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter if attr is None else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

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

        _, attr = self.columns[index.column()]

        if attr == "Entregada":
            return (
                    Qt.ItemFlag.ItemIsEnabled |
                    Qt.ItemFlag.ItemIsUserCheckable |
                    Qt.ItemFlag.ItemIsSelectable
            )

        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

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

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False

        row = index.row()
        column = index.column()
        _, attr = self.columns[column]

        if attr == "Entregada" and role == Qt.ItemDataRole.CheckStateRole:
            usuario = self._data[row]
            new_value = value == Qt.CheckState.Checked
            setattr(usuario, attr, new_value)

            # Guardar inmediatamente en DB
            #from src.db.db_manager import DBManager
            #DBManager().update(usuario)
            self.dao.update(usuario)

            self.dataChanged.emit(index, index, [role])
            return True

        return False


