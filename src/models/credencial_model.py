from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, inspect
)
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.config.database_config import Base, SessionLocal


# Modelo ORM de Usuario
class TbcUsuarios(Base):
    __tablename__ = 'TbcUsuarios'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FolioId = Column(String(25))
    Nombre = Column(String(100), nullable=False, default="")
    Paterno = Column(String(100), nullable=False, default="")
    Materno = Column(String(100), nullable=False, default="")
    FechaNacimiento = Column(Date, nullable=False)
    Genero = Column(String(10), nullable=False, default="")
    CURP = Column(String(20), nullable=False, default="")
    Calle = Column(String(100), nullable=False, default="")
    NumExterior = Column(String(10), nullable=False, default="")
    NumInterior = Column(String(10), nullable=False, default="")
    Manzana = Column(String(10), nullable=False, default="")
    Lote = Column(String(10), nullable=False, default="")
    Colonia = Column(String(100), nullable=False, default="")
    CodigoPostal = Column(String(10), nullable=False, default="")
    Municipio = Column(String(100), nullable=False, default="")
    Entidad = Column(String(20), nullable=False, default="")
    Celular = Column(String(10), nullable=False, default="")
    Email = Column(String(100), nullable=False, default="")
    SeccionElectoral = Column(String(20), nullable=False, default="")

    Responsable = Column(String(50), nullable=False, default="")

    RutaFoto = Column(String(255), nullable=False, default="")
    RutaFirma = Column(String(200), nullable=False, default="")
    RutaQR = Column(String(200), nullable=False, default="")

    NumImpresion = Column(Integer)
    FechaAlta = Column(Date)
    VecesImpresa = Column(Integer, default=0)
   # Entregada = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Usuario {self.FolioId} - {self.Nombre} {self.Paterno}>"

    def _set_date(self, attribute: str, value):
        """Converts a string to a date and assigns it to the attribute."""
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠️ Invalid date for {attribute}: {value}")
                return
        setattr(self, attribute, value)

    def set_birth_date(self, value):
        self._set_date("BirthDate", value)

    def set_registration_date(self, value):
        self._set_date("RegistrationDate", value)


# DAO para TbcUsuarios
class TbcUsuariosDAO:
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def get_all(self):
        try:
            with self.session_factory() as session:
                return session.query(TbcUsuarios).all()
        except SQLAlchemyError as e:
            print(f"⚠️ Error al obtener todos los usuarios: {e}")
            return []

    def get_filter(self, texto_busqueda=""):
        try:
            with self.session_factory() as session:
                query = session.query(TbcUsuarios)
                if texto_busqueda:
                    query = query.filter(
                        TbcUsuarios.Nombre.ilike(f"%{texto_busqueda}%") |
                        TbcUsuarios.CURP.ilike(f"%{texto_busqueda}%")
                    )
                return query.all()
        except SQLAlchemyError as e:
            print(f"⚠️ Error al filtrar usuarios: {e}")
            return []

    def update(self, usuario ):
        """Actualiza un registro de TbcUsuarios en la base de datos."""
        session = self.session_factory()
        try:
            existing = session.query(TbcUsuarios).filter_by(Id=usuario.Id).one()
            for attr in vars(usuario):
                if attr.startswith("_"):
                    continue
                if hasattr(existing, attr):
                    setattr(existing, attr, getattr(usuario, attr))
            session.commit()
            return True
        except NoResultFound:
            print(f"[ERROR] Usuario con ID {usuario.Id} no encontrado.")
        except SQLAlchemyError as e:
            print(f"[ERROR] Error al actualizar usuario: {e}")
            session.rollback()
        finally:
            session.close()
        return False


# 🔍 Funciones de validación para estructura de base de datos

def obtener_campos_modelo():
    """Devuelve los nombres de los campos del modelo TbcUsuarios."""
    return TbcUsuarios.__table__.columns.keys()


def limpiar_datos_entrada(datos: dict) -> dict:
    """Filtra las claves de un diccionario para que coincidan con los campos del modelo."""
    campos_validos = obtener_campos_modelo()
    return {k: v for k, v in datos.items() if k in campos_validos}


def verificar_estructura_base(session) -> bool:
    """Verifica que todos los campos del modelo existan en la tabla."""
    try:
        campos_modelo = set(obtener_campos_modelo())
        campos_db = set(col[1] for col in session.execute("PRAGMA table_info('TbcUsuarios')"))
        faltantes = campos_modelo - campos_db
        if faltantes:
            print(f"⚠️ Faltan campos en la base: {faltantes}")
            return False
        return True
    except Exception as e:
        print(f"⚠️ Error verificando estructura: {e}")
        return False


def validar_estructura(engine) -> bool:
    """Verifica que la tabla TbcUsuarios exista en la base."""
    try:
        inspector = inspect(engine)
        return "TbcUsuarios" in inspector.get_table_names()
    except Exception as e:
        print(f"⚠️ Error inspeccionando tabla: {e}")
        return False


def validar_columnas(engine) -> bool:
    """Verifica que existan las columnas mínimas requeridas."""
    columnas_requeridas = {"Nombre", "Paterno", "Materno", "CURP"}
    try:
        inspector = inspect(engine)
        columnas_actuales = {col["name"] for col in inspector.get_columns("TbcUsuarios")}
        return columnas_requeridas.issubset(columnas_actuales)
    except Exception as e:
        print(f"⚠️ Error validando columnas: {e}")
        return False
