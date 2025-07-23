from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Date, Boolean, inspect
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.config.database_config import Base, SessionLocal


# Modelo ORM de Usuario
class TbcUsuarios(Base):
    __tablename__ = 'TbcUsuarios'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    FolioId = Column(String(25))
    Nombre = Column(String(100), nullable=False)
    Paterno = Column(String(100))
    Materno = Column(String(100))
    FechaNacimiento = Column(Date)
    Genero = Column(String(10))
    CURP = Column(String(20))
    Calle = Column(String(100))
    NumExterior = Column(String(10))
    NumInterior = Column(String(10))
    Manzana = Column(String(10))
    Lote = Column(String(10))
    Colonia = Column(String(100))
    CodigoPostal = Column(String(10))
    Municipio = Column(String(100))
    EntidadId = Column(Integer)
    Celular = Column(String(20))
    Email = Column(String(100))
    SeccionElectoral = Column(String(50))
    RutaFoto = Column(String(255))
    RutaFirma = Column(String(200))
    RutaQR = Column(String(200))
    NumImpresion = Column(Integer)
    FechaAlta = Column(Date)
    CredencialImpresa = Column(Boolean, default=False)
    Entregada = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Usuario {self.FolioId} - {self.Nombre} {self.Paterno}>"

    def _set_fecha(self, atributo: str, valor):
        """Convierte una cadena a fecha y la asigna al atributo."""
        if isinstance(valor, str):
            try:
                valor = datetime.strptime(valor, "%Y-%m-%d").date()
            except ValueError:
                print(f"⚠️ Fecha inválida para {atributo}: {valor}")
                return
        setattr(self, atributo, valor)

    def set_FechaNacimiento(self, valor): self._set_fecha("FechaNacimiento", valor)
    def set_FechaAlta(self, valor): self._set_fecha("FechaAlta", valor)


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
