# src/controllers/main_controller.py
import csv
import logging
import shutil
from pathlib import Path

import pandas as pd
from datetime import datetime

from PySide6.QtGui import QPixmap, Qt, QPainter, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QMessageBox, QMainWindow, QHeaderView, QFileDialog, QAbstractItemView, QTableView
from sqlalchemy import func

from sqlalchemy.inspection import inspect

from src.controllers.capture_controller import CaptureController
from src.controllers.edit_controller import EditController
from src.controllers.modulo_dialog import crear_base_si_no_existe
from src.controllers.previsualizacion_controller import PreviewController
from src.database.db_manager import DBManager
from src.delegates.action_delegate import ActionDelegate, CheckboxColorDelegate
from src.models.credencial_model import TbcUsuarios, TbcUsuariosDAO
from src.models.usuarios_table_model import UsuariosTableModel
from src.utils.helpers import sanitize_data, clean_empty_strings, set_svg_icon
from src.utils.icons_utils import set_svg_icons
from src.utils.rutas import get_bd_path, get_icons_path, get_exportaciones_dir, get_foto_dir

from src.views.ventana_principal import Ui_MainWindow




def sanitize_value(value):
    """Convierte NaN y None en '', limpia strings, mantiene fechas y bools."""
    if pd.isna(value):
        return ""
    if isinstance(value, str):
        return value.strip()
    return value


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
        'CREDENCIAL IMPRESA': 'CredencialImpresa',
        'ENTREGADA': 'Entragada'
    }

    for excel_col, attr in fields_mapping.items():
        raw_value = row.get(excel_col)

        if attr in ["FechaNacimiento", "FechaAlta"]:
            try:
                if isinstance(raw_value, str):
                    raw_value = raw_value.strip()
                    value = datetime.strptime(raw_value, "%d/%m/%Y").date()
                elif isinstance(raw_value, pd.Timestamp):
                    value = raw_value.date()
                else:
                    value = None
            except Exception:
                value = None
        elif attr in ["CredencialImpresa", "Entragada"]:
            value = str(raw_value).strip().lower() in ["sí", "si", "1", "true", "x"]
        else:
            value = sanitize_value(raw_value)

        # Evitar guardar 'nan' como string literal
        if isinstance(value, str) and value.lower() == "nan":
            value = ""

        setattr(users, attr, value)

    users.FolioId = db.generate_folio(consecutivo_directo=folio_directo)
    users.FechaAlta = datetime.today().date()
    clean_empty_strings(users)

    return users


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.check_box_credential_delivered = None

        # Cargar UI
        self.mw = Ui_MainWindow()
        self.ui = self.mw
        self.ui.setupUi(self)

        # Verificar base de datos disponible
        self.db_path = get_bd_path()
        if not self.db_path:
            QMessageBox.warning(self, "Sin bases", "No se encontró base de datos en la carpeta.")
            return

        self.db = DBManager()

        crear_base_si_no_existe()

        # Cargar logo
        self._cargar_logo()

        # Controladores
        self.preview_ctrl = PreviewController(self.ui, self.db)
        self.capture_controller = CaptureController(self.mw, self.ui, self.db, self.preview_ctrl)
        self.edit_ctrl = EditController(self, self.capture_controller)

        # DAO y delegados
        self.delegate_configured = False

        # Conexiones principales
        self.capture_controller.updated_credential.connect(self.reload_table)
        self.ui.searchBar.textChanged.connect(self.reload_table)

        set_svg_icon(self.ui.captureBtn, "capture.svg", QSize(24, 24))
        self.ui.captureBtn.clicked.connect(self.show_capture_form)

        set_svg_icon(self.ui.homeBtn, "home.svg", QSize(24, 24))
        self.ui.homeBtn.clicked.connect(self.view_home)

        set_svg_icon(self.ui.importBtn, "database-import.svg", QSize(24, 24))
        self.ui.importBtn.clicked.connect(self.import_excel)



        self.model_db = TbcUsuariosDAO()
        set_svg_icon(self.ui.exportBtn, "database-export.svg", QSize(24, 24))
        self.ui.exportBtn.clicked.connect(self.exportar_base_y_fotos)

        #Prueba para poner todos los iconos
        self.set_icons = set_svg_icons(self.ui)


        # Cargar vista inicial
        self.reload_table()
        self.view_home()

    def _cargar_logo(self):
        """Carga y ajusta el logo en el QLabel correspondiente."""
        logo_path = get_icons_path("Logo_Famc.png")
        if not logo_path.exists():
            print("[⚠️] Logo no encontrado:", logo_path)
            return
        # Establecer el ícono de la ventana principal
        icono = QIcon(str(logo_path))  # Cambia la ruta al archivo de tu ícono
        self.setWindowIcon(icono)

        # El resto de tu configuración de la ventana (título, tamaño, etc.)
        self.setWindowTitle("Sistema Familia Cuajimalpa")

        pixmap = QPixmap(logo_path)
        label = self.ui.labelSistemaCuajimalpa

        scale_factor = min(
            label.width() / pixmap.width(),
            label.height() / pixmap.height()
        )
        new_size = pixmap.size() * scale_factor

        scaled_pixmap = pixmap.scaled(
            new_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def load_table(self):
        """Carga y filtra las credenciales en la tabla."""
        search_text = self.ui.searchBar.text().lower()
        credentials = self.db.obtener_todas()

        if search_text:
            credentials = [
                c for c in credentials if any(
                    search_text in str(getattr(c, attr, "")).lower()
                    for attr in ["Nombre", "Paterno", "Materno", "CURP", "FolioId"]
                )
            ]

        model = UsuariosTableModel(credentials, self.model_db)
        self.ui.usersTableView.setModel(model)

        if not self.delegate_configured:
            self._configurar_delegados(model)
            self.delegate_configured = True

    def _configurar_delegados(self, model):
        """Configura los delegados de la tabla por primera vez."""
        table = self.ui.usersTableView

        # Acciones
        self.action_delegate = ActionDelegate(table)
        table.setItemDelegateForColumn(6, self.action_delegate)

        # Permitir edición

        # Conectar acciones
        self.action_delegate.editarClicked.connect(self.edit_user_by_row)
        self.action_delegate.verClicked.connect(self.show_user_by_row)


    def show_capture_form(self):
        """Prepara el formulario para una nueva captura."""
        self.capture_controller.edition_mode = False
        self.capture_controller.credential_editing = None
        self.capture_controller.clear_form()
        self.ui.usersTableView.clearSelection()

        # Reinicia correctamente el estado de la cámara
        self.capture_controller.camera_ctrl.prepare_photo_state()
        #self.capture_controller.signature_ctrl.prepare_signature_state()
        self.ui.stackedWidget.setCurrentWidget(self.ui.captureView)

    def view_home(self):
        """Muestra la vista de inicio y detiene cualquier cámara activa."""
        self.capture_controller.camera_ctrl.prepare_photo_state()
        #self.capture_controller.signature_ctrl.prepare_signature_state()


        self._configure_user_table()
        self.ui.stackedWidget.setCurrentWidget(self.ui.homeView)

    def edit_user_by_row(self, row):
        """Carga una credencial para edición."""
        self.capture_controller.camera_ctrl.prepare_photo_state()
       # self.capture_controller.signature_ctrl.prepare_signature_state()

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
                    # Convierte la fila de pandas a diccionario y límpiala
                    raw_data = row.to_dict()
                    clean_data = sanitize_data(raw_data)

                    # Genera folio
                    consecutive_folio = db_consecutive + offset + 1

                    # Crea el objeto usuario limpio
                    excel_users = row_to_user(clean_data, self.db, consecutive_folio)
                    users.append(excel_users)

                except Exception as e:
                    print(f"❌ Error en fila {offset + 1}: {e}")

            self.db.insertar_multiples(users)
            self.reload_table()

            QMessageBox.information(self, "Importación completada",
                                    f"{len(users)} credenciales importadas correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error al importar", str(e))

    def reload_table(self):
        self.load_table()

    def exportar_base_y_fotos(self):
        model_dao = self.model_db

        export_dir = get_exportaciones_dir()
        export_csv_path = export_dir / "base_exportada.csv"
        export_fotos_dir = export_dir / "fotos"

        export_dir.mkdir(parents=True, exist_ok=True)
        export_fotos_dir.mkdir(parents=True, exist_ok=True)

        # Obtener todos los usuarios
        usuarios = model_dao.get_all()
        if not usuarios:
            print("[Exportación] No hay usuarios en la base de datos.")
            QMessageBox.critical(self, "Error al importar", "[Exportación] No hay usuarios en la base de datos.")
            return

        # Obtener nombres de columnas del modelo automáticamente
        columnas = [col.name for col in inspect(TbcUsuarios).columns]

        with open(export_csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columnas)

            for u in usuarios:
                datos = [getattr(u, col, "") for col in columnas]
                writer.writerow(datos)

                # Copiar la foto si existe
                if u.RutaFoto:
                    origen = Path(u.RutaFoto)
                    destino = export_fotos_dir / origen.name

                    try:
                        if origen.exists():
                            shutil.copyfile(origen, destino)
                            print(f"[Exportación] Foto exportada: {destino.name}")
                    except Exception as e:
                        print(f"[Exportación] Error al copiar la foto {origen.name}: {e}")

        QMessageBox.information(self, "Base exportada correctamente a",f" {export_csv_path}.")

        QMessageBox.information(self, "Fotos exportadas a",f" {export_fotos_dir}.")

