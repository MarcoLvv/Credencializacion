# src/controllers/main_controller.py
import os
from pathlib import Path

import pandas as pd
from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox, QMainWindow, QHeaderView, QFileDialog, QInputDialog


from src.controllers.capture_controller import CaptureController
from src.controllers.edit_controller import EditController
from src.controllers.previsualizacion_controller import PrevisualizacionController
from src.database.db_manager import DBManager
from src.delegates.action_delegate import ActionDelegate
from src.models.credencial_model import TbcUsuarios, TbcUsuariosDAO
from src.models.usuarios_table_model import UsuariosTableModel
from src.utils.rutas import get_bd_path, get_data_db_dir, get_data_dir
from src.views.ventana_principal import Ui_MainWindow


def fila_a_usuario(row, db, folio_directo=None):
    usuario = TbcUsuarios()
    mapeo_campos = {
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


    for excel_col, attr in mapeo_campos.items():
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
        self.db_path = get_bd_path()
        if not self.db_path:
            QMessageBox.warning(self, "Sin bases", "No se encontro base de datos en la carpeta.")
            return

        self.db = DBManager()


        # Inicializar controladores con DB ya configurada

        self.preview_ctrl = PrevisualizacionController(self.ui)
        self.capture_controller = CaptureController(self.mw, self.ui, self.db, self.preview_ctrl)
        self.edit_ctrl = EditController(self, self.capture_controller)


        # Crear instancia DBManager con la ruta de la base inicial
        self.capture_controller.actualizar_db(self.db)

        # Conexiones de botones
        self.capture_controller.credencial_actualizada.connect(self.recargar_tabla)
        self.ui.searchBar.textChanged.connect(self.recargar_tabla)
        self.ui.btnCapturar.clicked.connect(self.mostrar_formulario_captura)
        self.ui.btnInicio.clicked.connect(self.mostrar_home)
        self.ui.btnImportar.clicked.connect(self.importar_excel)

        # Conexión del ComboBox para cambiar base

        self.model_db = TbcUsuariosDAO()
        self.delegate_configurado = False

        self.recargar_tabla()
        self.mostrar_home()


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
        self.capture_controller.camera_ctrl.preparar_estado_captura()
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)

        self.edit_ctrl.mostrar_formulario_captura(credencial)
        self.ui.stackedWidget.setCurrentWidget(self.ui.viewCaptura)

    def ver_usuario_por_fila(self, fila):
        """Muestra una credencial en modo previsualización."""
        model = self.ui.usuariosVista.model()
        credencial = model.obtener_datos_fila(fila)
        print(model)
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
            self.recargar_tabla()

            QMessageBox.information(self, "Importación completada",
                                    f"{len(usuarios)} credenciales importadas correctamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error al importar", str(e))

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




