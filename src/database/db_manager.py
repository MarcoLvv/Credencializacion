from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.config.database_config import Base
from src.models.credencial_model import TbcUsuarios
from src.utils.config_manager import get_module_id
from src.utils.rutas import get_data_dir


def crear_base_de_datos(path_db):
    """Crea una base de datos SQLite nueva y genera sus tablas."""
    engine_nuevo = create_engine(f"sqlite:///{str(path_db)}")
    Base.metadata.create_all(bind=engine_nuevo)
    return engine_nuevo


class DBManager:
    def __init__(self, ruta_db=None):
        # Si no se proporciona ruta, por defecto data/base.db
        self.ruta_db = Path(ruta_db) if ruta_db else get_data_dir() / "base.db"

        self.engine = create_engine(f"sqlite:///{str(self.ruta_db)}")

        self.Session = sessionmaker(bind=self.engine)

        # Crear base si no existe
        if not self.ruta_db.exists():
            print(f"[DB] Base no encontrada. Creando nueva base: {self.ruta_db}")
            Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.Session()

    def cambiar_base(self, nueva_ruta):
        nueva_ruta = Path(nueva_ruta)  # Asegurar que es Path
        if not nueva_ruta.exists():
            print(f"[DBManager] ⚠️ La ruta {nueva_ruta} no existe. ¿Deseas crear una nueva base?")
            crear_base_de_datos(nueva_ruta)

        self.ruta_db = nueva_ruta
        self.engine = create_engine(f"sqlite:///{str(self.ruta_db)}")  # 👈 Conversión importante
        self.Session = sessionmaker(bind=self.engine)

    def crear_base_nueva(self, nombre_archivo):
        """
        Crea una nueva base con el nombre proporcionado dentro de /data/bases
        """
        ruta = get_data_dir() / f"{nombre_archivo}.db"
        if ruta.exists():
            print(f"[DBManager] ⚠️ La base {ruta.name} ya existe.")
            return False
        crear_base_de_datos(ruta)
        self.cambiar_base(ruta)
        print(f"[DBManager] ✅ Nueva base creada y activada: {ruta.name}")
        return True

    def get_next_consecutive(self):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar() or 0
            return f"{count + 1:05d}"

    def get_last(self):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar() or 0
            return f"{count:05d}"

    def generar_folio(self):
        now = datetime.now()
        año = now.strftime("%Y")
        mes = now.strftime("%m")
        modulo = get_module_id()
        consecutivo = self.get_next_consecutive()
        return f"FAMC-{año}{mes}-{modulo}-{consecutivo}"

    def insertar_credencial(self, **datos):
        folio = self.generar_folio()
        cred = TbcUsuarios(
            FolioId=folio,
            Nombre=datos.get("Nombre", ""),
            Paterno=datos.get("Paterno", ""),
            Materno=datos.get("Materno", ""),
            CURP=datos.get("CURP", ""),
            FechaNacimiento=datos.get("fechaNacimiento"),
            Calle=datos.get("Calle", ""),
            Lote=datos.get("Lote", ""),
            Manzana=datos.get("Manzana", ""),
            NumExterior=datos.get("NumExterior", ""),
            NumInterior=datos.get("NumInterior", ""),
            Colonia=datos.get("Colonia", ""),
            CodigoPostal=datos.get("CodigoPostal", ""),
            Municipio=datos.get("Municipio", ""),
            SeccionElectoral=datos.get("SeccionElectoral", ""),
            Genero=datos.get("Genero", ""),
            Celular=datos.get("Celular", ""),
            Email=datos.get("Email", ""),
            RutaFoto=datos.get("ruta_foto", ""),
            RutaFirma=datos.get("ruta_firma", ""),
            RutaQR=datos.get("ruta_qr", "")
        )
        with self.Session() as session:
            session.add(cred)
            session.commit()
        return folio

    def insertar_multiples(self, lista_credenciales):
        with self.Session() as session:
            session.add_all(lista_credenciales)
            session.commit()

    def actualizar_ruta_foto(self, folio, nueva_ruta):
        with self.Session() as session:
            cred = session.query(TbcUsuarios).filter_by(FolioId=folio).first()
            if cred:
                cred.RutaFoto = nueva_ruta
                session.commit()
                return True
            return False

    def actualizar_credencial(self, folio, **datos_actualizados):
        with self.Session() as session:
            print("DEBUG - folio recibido:", folio, type(folio))

            if isinstance(folio, list):
                folio = folio[0]  # si es lista, tomamos el primer valor
            # Ahora folio es un valor plano
            cred = session.query(TbcUsuarios).filter_by(FolioId=folio).first()

            if not cred:
                print(f"[ERROR] No se encontró credencial con folio: {folio}")
                return False
            for campo, valor in datos_actualizados.items():
                if hasattr(cred, campo):
                    setattr(cred, campo, valor)
            session.commit()
            return True

    def eliminar_credencial(self, id_credencial):
        with self.Session() as session:
            cred = session.query(TbcUsuarios).filter_by(Id=id_credencial).first()
            if cred:
                session.delete(cred)
                session.commit()
                return True
            return False

    def obtener_todas(self):
        with self.Session() as session:
            return session.query(TbcUsuarios).all()

    def obtener_por_id(self, id_credencial):
        with self.Session() as session:
            return session.query(TbcUsuarios).filter_by(Id=id_credencial).first()

    def obtener_por_nombre(self, nombre):
        with self.Session() as session:
            return session.query(TbcUsuarios).filter_by(Nombre=nombre).first()

    def obtener_credencial(self):
        with self.Session() as session:
            return session.query(TbcUsuarios)
