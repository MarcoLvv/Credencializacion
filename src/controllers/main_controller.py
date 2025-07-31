# src/controllers/main_controller.py
import pandas as pd
from datetime import datetime

from PySide6.QtWidgets import QMessageBox, QMainWindow, QHeaderView, QFileDialog
from sqlalchemy import func

from src.controllers.capture_controller import CaptureController
from src.controllers.edit_controller import EditController
from src.controllers.previsualizacion_controller import PreviewController
from src.database.db_manager import DBManager
from src.delegates.action_delegate import ActionDelegate
from src.models.credencial_model import TbcUsuarios, TbcUsuariosDAO
from src.models.usuarios_table_model import UsuariosTableModel
from src.utils.rutas import get_bd_path
from src.views.ventana_principal import Ui_MainWindow


def row_to_user(row, db, folio_directo=None):
    users = TbcUsuarios()
    fields_mapping = {
        'NOMBRE': 'Nombre',
        'APELLIDO PATERNO': 'Paterno',
        'APELLIDO MATERNO': 'Materno',
        'FECHA DE NACIMIENTO': 'FechaNacimiento',
        'CALLE': 'Calle',
        'NUMERO': 'NumExterior',
        'COLONIA': 'Colonia',
        'MUNICIPIO/ALCALDIA': 'Municipio',
        'CURP': 'CURP',
        'SECCION': 'SeccionElectoral',
        'FOTOGRAFIA': 'RutaFoto',
        'TELEFONO': 'Celular',
        'CORREO': 'Email',
        'RESPONSABLE': 'Responsable',
        'CREDENCIAL IMPRESA': 'CredencialImpresa',  # Si lo activas después
        'ENTREGADA': 'Entragada'  # Si lo activas después
    }


    for excel_col, attr in fields_mapping.items():
        if pd.isna(row.get(excel_col)):
            setattr(users, attr, None)
        else:
            value = row[excel_col]
            if attr in ["FechaNacimiento", "FechaAlta"]:
                try:
                    if isinstance(value, str):
                        value = datetime.strptime(value, "%d/%m/%Y").date()
                    elif isinstance(value, pd.Timestamp):
                        value = value.date()
                except Exception:
                    value = None  # Fecha malformada

            elif attr in ["CredencialImpresa", "Entragada"]:
                value = str(value).strip().lower() in ["sí", "si", "1", "true", "x"]

            setattr(users, attr, value)
        pass

    # ✅ Generar folio con lógica correcta
    users.FolioId = db.generate_folio(consecutivo_directo=folio_directo)
    users.FechaAlta = datetime.today().date()
    return users

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mw = Ui_MainWindow()
        self.ui = self.mw
        self.ui.setupUi(self)

        # Inicializar rutas de bases de datos disponibles
        self.db_path = get_bd_path()
        if not self.db_path:
            QMessageBox.warning(self, "Sin bases", "No se encontro base de datos en la carpeta.")
            return

        self.db = DBManager()


        # Inicializar controladores con DB ya configurada

        self.preview_ctrl = PreviewController(self.ui)
        self.capture_controller = CaptureController(self.mw, self.ui, self.db, self.preview_ctrl)
        self.edit_ctrl = EditController(self, self.capture_controller)

        # Crear instancia DBManager con la ruta de la base inicial
        #self.capture_controller.update_db(self.db)

        # Conexiones de botones
        self.capture_controller.updated_credential.connect(self.reload_table)
        self.ui.searchBar.textChanged.connect(self.reload_table)
        self.ui.captureBtn.clicked.connect(self.show_capture_form)
        self.ui.homeBtn.clicked.connect(self.view_home)
        self.ui.importBtn.clicked.connect(self.import_excel)

        # Conexión del ComboBox para cambiar base

        self.model_db = TbcUsuariosDAO()
        self.delegate_configured = False

        self.reload_table()
        self.view_home()


    def load_table(self):
        """Carga las credenciales y las muestra en la tabla, aplicando filtro si hay texto."""
        search_text = self.ui.searchBar.text().lower()
        credentials = self.db.obtener_todas()

        if search_text:
            credentials = [
                c for c in credentials if any(
                    search_text in str(getattr(c, attr, "")).lower()
                    for attr in ["Nombre", "Paterno", "Materno", "CURP", "FolioId"]
                )
            ]

        model = UsuariosTableModel(credentials)
        self.ui.usersTableView.setModel(model)

        if not self.delegate_configured:
            self.action_delegate = ActionDelegate(self.ui.usersTableView)
            self.ui.usersTableView.setItemDelegateForColumn(6, self.action_delegate)
            self.action_delegate.editarClicked.connect(self.edit_user_by_row)
            self.action_delegate.verClicked.connect(self.show_user_by_row)
            self.delegate_configured = True

    def show_capture_form(self):
        """Prepara el formulario para una nueva captura."""
        self.capture_controller.edition_mode = False
        self.capture_controller.credential_editing = None
        self.capture_controller.clear_form()
        self.ui.usersTableView.clearSelection()

        # Reinicia correctamente el estado de la cámara
        self.capture_controller.camera_ctrl.prepare_capture_state()

        self.ui.stackedWidget.setCurrentWidget(self.ui.captureView)

    def view_home(self):
        """Muestra la vista de inicio y detiene cualquier cámara activa."""
        self.capture_controller.camera_ctrl.prepare_capture_state()


        self._configure_user_table()
        self.ui.stackedWidget.setCurrentWidget(self.ui.homeView)

    def edit_user_by_row(self, row):
        """Carga una credencial para edición."""
        self.capture_controller.camera_ctrl.prepare_capture_state()
        model = self.ui.usersTableView.model()
        credential = model.get_row_data(row)

        self.edit_ctrl.show_capture_form(credential)
        self.ui.stackedWidget.setCurrentWidget(self.ui.captureView)

    def show_user_by_row(self, row):
        """Muestra una credencial en modo previsualización."""
        model = self.ui.usersTableView.model()
        credential = model.get_row_data(row)
        print(model)
        self.preview_ctrl.show_credential(credential)
        self.ui.stackedWidget.setCurrentWidget(self.ui.credentialView)

    def _configure_user_table(self):
        """Ajusta el tamaño de columnas de la tabla de usuarios."""
        header = self.ui.usersTableView.horizontalHeader()
        self.ui.usersTableView.verticalHeader().setVisible(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

    def import_excel(self):
        excel_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "",
                                              "Excel (*.xlsx *.xls);;CSV (*.csv)")
        if not excel_path:
            return

        try:
            df = pd.read_excel(excel_path) if excel_path.endswith(".xlsx") else pd.read_csv(excel_path)

            # Obtener base del consecutivo
            with self.db.Session() as session:
                db_consecutive = session.query(func.count(TbcUsuarios.Id)).scalar() or 0

            users = []
            for offset, (_, row) in enumerate(df.iterrows()):
                try:
                    consecutive_folio = db_consecutive + offset + 1
                    excel_users = row_to_user(row, self.db, consecutive_folio)
                    users.append(excel_users)
                except Exception as e:
                    print(f"❌ Error en fila: {e}")

            self.db.insertar_multiples(users)
            self.reload_table()

            QMessageBox.information(self, "Importación completada",
                                    f"{len(users)} credenciales importadas correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error al importar", str(e))

    def reload_table(self):
        self.load_table()

    def load_users(self):
        users = self.model_db.get_all()
        model = UsuariosTableModel(users)
        self.ui.usersTableView.setModel(model)

    def update_view(self):
        if not self.db.Session:
            print("⚠️ No hay sesión activa.")
            return

        try:
            dao = TbcUsuariosDAO(self.db.get_session)
            users = dao.get_all()
            model = UsuariosTableModel(users)
            self.ui.usersTableView.setModel(model)
            self.ui.usersTableView.resizeColumnsToContents()
        except Exception as e:
            print(f"⚠️ Error actualizando vista: {e}")




