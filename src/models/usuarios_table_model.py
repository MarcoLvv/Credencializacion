# src/models/usuarios_table_model.py
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class UsuariosTableModel(QAbstractTableModel):
    """
    Modelo de tabla para mostrar usuarios en una QTableView.
    Usa una lista de objetos con atributos (ej. instancia de TbcUsuarios).
    """

    def __init__(self, data=None):
        super().__init__()
        self._data = data or []

        # Map headers -> atributo del modelo
        self.columns = [
            ("ID", "Id"),
            ("Folio", "FolioId"),
            ("Nombre", "Nombre"),
            ("Paterno", "Paterno"),
            ("Materno", "Materno"),
            ("Sección Electoral", "SeccionElectoral"),
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        usuario = self._data[index.row()]
        _, attr = self.columns[index.column()]
        valor = getattr(usuario, attr, "")
        return str(valor) if valor is not None else ""

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.columns[section][0]
        elif orientation == Qt.Orientation.Vertical:
            return str(section + 1)
        return None

    def update_data(self, new_data):
        """Recarga el modelo con nuevos datos."""
        self.beginResetModel()
        self._data = new_data or []
        self.endResetModel()

    def obtener_datos_fila(self, row):
        """Devuelve el objeto de la fila (ej. un TbcUsuario)."""
        if 0 <= row < len(self._data):
            return self._data[row]
        return None
