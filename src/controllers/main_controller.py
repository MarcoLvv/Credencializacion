# src/controllers/main_controller.py
import os
from pathlib import Path

import pandas as pd
from datetime import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QMessageBox, QMainWindow, QHeaderView, QFileDialog, QInputDialog
from sqlalchemy import create_engine, func

from src.controllers.capture_controller import CaptureController
from src.controllers.edit_controller import EditController
from src.controllers.previsualizacion_controller import PrevisualizacionController
from src.database.db_manager import DBManager
from src.delegates.action_delegate import ActionDelegate
from src.models.credencial_model import TbcUsuarios, TbcUsuariosDAO
from src.models.usuarios_table_model import UsuariosTableModel
from src.utils.rutas import get_bases_disponibles, get_bd_path, get_data_db_dir
from src.views.ventana_principal import Ui_MainWindow


def fila_a_usuario(row, db, folio_directo=None):
    usuario = TbcUsuarios()
    CAMPOS_MAPPINGS = {
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
        'CREDENCIAL IMPRESA': 'CredencialImpresa',  # Si lo activas después
        'ENTREGADA': 'Entragada'  # Si lo activas después
    }


    for excel_col, attr in CAMPOS_MAPPINGS.items():
        if pd.isna(row.get(excel_col)):
            setattr(usuario, attr, None)
        else:
            valor = row[excel_col]
            if attr in ["FechaNacimiento", "FechaAlta"]:
                try:
                    if isinstance(valor, str):
                        valor = datetime.strptime(valor, "%d/%m/%Y").date()
                    elif isinstance(valor, pd.Timestamp):
                        valor = valor.date()
                except Exception:
                    valor = None  # Fecha malformada

            elif attr in ["CredencialImpresa", "Entragada"]:
                valor = str(valor).strip().lower() in ["sí", "si", "1", "true", "x"]

            setattr(usuario, attr, valor)
        pass

    # ✅ Generar folio con lógica correcta
    usuario.FolioId = db.generar_folio(consecutivo_directo=folio_directo)
    usuario.FechaAlta = datetime.today().date()
    return usuario

class VistaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mw = Ui_MainWindow()
        self.ui = self.mw
        self.ui.setupUi(self)

        # Inicializar rutas de bases de datos disponibles
        self.db_paths = get_bases_disponibles()
        if not self.db_paths:
            QMessageBox.warning(self, "Sin bases", "No se encontraron bases de datos en la carpeta.")
            return

        # Establecer base inicial (la primera del comboBox)
        base_inicial = self.db_paths[0]
        self.ui.comboBoxDB.addItems(self.db_paths)

        self.db = DBManager(base_inicial)

        # Inicializar controladores con DB ya configurada
        self.capture_controller = CaptureController(self.mw, self.ui, self.db)
        self.edit_ctrl = EditController(self, self.capture_controller)
        self.preview_ctrl = PrevisualizacionController(self.ui)


        # Crear instancia DBManager con la ruta de la base inicial
        self.capture_controller.actualizar_db(self.db)

        # Conexiones de botones
        self.capture_controller.credencial_actualizada.connect(self.load_table)
        self.ui.searchBar.textChanged.connect(self.load_table)
        self.ui.btnCapturar.clicked.connect(self.mostrar_formulario_captura)
        self.ui.btnInicio.clicked.connect(self.mostrar_home)
        self.ui.btnImportar.clicked.connect(self.importar_excel)
        self.ui.btnNuevaBase.clicked.connect(self.crear_nueva_base)

        # Conexión del ComboBox para cambiar base
        self.ui.comboBoxDB.currentIndexChanged.connect(self.cambiar_base_desde_combo)

        self.model_db = TbcUsuariosDAO()
        self.delegate_configurado = False

        self.load_table()
        self.mostrar_home()

    def cambiar_base_desde_combo(self):
        nombre_archivo = self.ui.comboBoxDB.currentText()
        ruta_nueva = get_bd_path() / nombre_archivo
        self.cambiar_y_cargar_base(ruta_nueva)

    def cargar_bases(self):
        self.ui.comboBoxDB.clear()

        directorio = get_data_db_dir()
        bases = [f for f in os.listdir(directorio) if f.endswith(".db")]

        self.ui.comboBoxDB.addItems(bases)

    def load_table(self):
        """Carga las credenciales y las muestra en la tabla, aplicando filtro si hay texto."""
        search_text = self.ui.searchBar.text().lower()
        credenciales = self.db.obtener_todas()

        if search_text:
            credenciales = [
                c for c in credenciales if any(
                    search_text in str(getattr(c, attr, "")).lower()
                    for attr in ["Nombre", "Paterno", "Materno", "CURP", "FolioId"]
                )
            ]

        model = UsuariosTableModel(credenciales)
        self.ui.usuariosVista.setModel(model)

        if not self.delegate_configurado:
            self.action_delegate = ActionDelegate(self.ui.usuariosVista)
            self.ui.usuariosVista.setItemDelegateForColumn(6, self.action_delegate)
            self.action_delegate.editarClicked.connect(self.editar_usuario_por_fila)
            self.action_delegate.verClicked.connect(self.ver_usuario_por_fila)
            self.delegate_configurado = True

    def crear_nueva_base(self):
        nombre, ok = QInputDialog.getText(self, "Nueva Base de Datos", "Nombre del archivo:")
        if ok and nombre.strip():
            nombre = nombre.strip()
            ruta_db = get_data_db_dir() / f"{nombre}.db"

            if ruta_db.exists():
                QMessageBox.warning(self, "Base existente", f"Ya existe una base con el nombre '{nombre}'.")
                return

            creada = self.db.crear_base_nueva(nombre)
            if creada:
                self.cargar_bases()
                self.ui.comboBoxDB.setCurrentText(nombre)
                # No se llama aquí a recargar_tabla() porque cambiar_base_desde_combo se disparará
            else:
                QMessageBox.critical(self, "Error", f"No se pudo crear la base '{nombre}'.")
        else:
            print("[INFO] Creación cancelada o nombre vacío.")

    def cambiar_y_cargar_base(self, ruta_db: Path):
        self.db = DBManager(ruta_db)
        self.capture_controller.db = self.db

        # Esperar breve tiempo antes de cargar tabla para evitar acceso prematuro
        QTimer.singleShot(100, self.load_table)

    def mostrar_formulario_captura(self):
        """Prepara el formulario para una nueva captura."""
        self.capture_controller.modo_edicion = False
        self.capture_controller.credencial_editando = None
        self.capture_controller.limpiar_formulario()
        self.ui.usuariosVista.clearSelection()

        # Reinicia correctamente el estado de la cámara
        self.capture_controller.camera_ctrl.preparar_estado_captura()

        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def mostrar_home(self):
        """Muestra la vista de inicio y detiene cualquier cámara activa."""
        self.capture_controller.camera_ctrl.preparar_estado_captura()


        self._configurar_tabla_usuarios()
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewHome)

    def editar_usuario_por_fila(self, fila):
        """Carga una credencial para edición."""
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)
        self.capture_controller.camera_ctrl.preparar_estado_captura()

        self.edit_ctrl._mostrar_formulario_captura(credencial)
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def ver_usuario_por_fila(self, fila):
        """Muestra una credencial en modo previsualización."""
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)
        self.preview_ctrl.mostrar_credencial(credencial)
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCredencial)

    def _configurar_tabla_usuarios(self):
        """Ajusta el tamaño de columnas de la tabla de usuarios."""
        header = self.ui.usuariosVista.horizontalHeader()
        self.ui.usuariosVista.verticalHeader().setVisible(False)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, 6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

    def importar_excel(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo Excel", "",
                                              "Excel (*.xlsx *.xls);;CSV (*.csv)")
        if not ruta:
            return

        try:
            df = pd.read_excel(ruta) if ruta.endswith(".xlsx") else pd.read_csv(ruta)

            # Obtener base del consecutivo
            from sqlalchemy import func
            with self.db.Session() as session:
                consecutivo_base = session.query(func.count(TbcUsuarios.Id)).scalar() or 0

            usuarios = []
            for offset, (_, row) in enumerate(df.iterrows()):
                try:
                    folio_consecutivo = consecutivo_base + offset + 1
                    usuario = fila_a_usuario(row, self.db, folio_consecutivo)
                    usuarios.append(usuario)
                except Exception as e:
                    print(f"❌ Error en fila: {e}")

            self.db.insertar_multiples(usuarios)
            self.load_table()

            QMessageBox.information(self, "Importación completada",
                                    f"{len(usuarios)} credenciales importadas correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error al importar", str(e))


        except Exception as e:
            QMessageBox.critical(self, "Error al importar", str(e))

    def cambiar_base_datos(self, nombre_base):

        # Construir ruta completa
        ruta = get_data_dir() / nombre_base  # o usa Path.joinpath si prefieres

        # Cambiar base de datos en DBManager
        self.db.cambiar_base(ruta)

        # Reconstruir sesión SQLAlchemy
        self.session = self.db.get_session()

        # Recargar el modelo con datos de la nueva base
        self.load_table()


    def recargar_tabla(self):
        self.load_table()

    def cargar_usuarios(self):
        session = self.db.get_session()
        usuarios = self.model_db.get_all()
        modelo = UsuariosTableModel(usuarios)
        self.ui.usuariosVista.setModel(modelo)

    def actualizar_vista(self):
        if not self.db.Session:
            print("⚠️ No hay sesión activa.")
            return

        try:
            dao = TbcUsuariosDAO(self.db.get_session)
            usuarios = dao.get_all()
            modelo = UsuariosTableModel(usuarios)
            self.ui.usuariosVista.setModel(modelo)
            self.ui.usuariosVista.resizeColumnsToContents()
        except Exception as e:
            print(f"⚠️ Error actualizando vista: {e}")

    #self.ui.btnCargarBase.clicked.connect(self.seleccionar_base_datos_existente)

    # def seleccionar_base_datos_existente(self):
    #     ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar base de datos", "", "Archivos SQLite (*.db)")
    #     if ruta:
    #         nombre = os.path.basename(ruta)
    #         destino = os.path.join(get_data_dir(), nombre)
    #         if not os.path.exists(destino):
    #             shutil.copy(ruta, destino)
    #         self.cargar_bases_disponibles()
    #         self.ui.comboBoxDB.setCurrentText(nombre)


