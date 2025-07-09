from PySide6.QtCore import QAbstractTableModel, Qt
from datetime import datetime
from sqlalchemy import create_engine, Integer, String, Column, Date, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql.sqltypes import Boolean

from src.config.database_config import Base, SessionLocal


def get_all():
    try:
        with SessionLocal() as session:
            return session.query(TbcUsuarios).all()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []


class TbcUsuariosModel:
    def get_filter(self, search_text=""):
        with SessionLocal() as session:
            query = session.query(TbcUsuarios)
            if search_text:
                query = query.filter(
                    TbcUsuarios.Nombre.ilike(f"%{search_text}%") |
                    TbcUsuarios.CURP.ilike(f"%{search_text}%")
                )
            return query.all()


class TbcUsuarios(Base):
    __tablename__ = 'TbcUsuarios'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    FolioId = Column(String(25))
    Nombre = Column(String(100), nullable=False)
    Paterno = Column(String(100))
    Materno = Column(String(100))
    FechaNacimiento = Column(Date)
    GeneroId = Column(Integer)
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
    RutaFoto = Column(String(255), nullable=True)
    RutaFirma = Column(String(200))  # Ruta donde se guarda la imagen PNG de la firma
    RutaQR = Column(String(200))
    NumImpresion = Column(Integer)
    FechaAlta = Column(Date)
    
    #AGREGAR CAMPOS CORRECTAMENTE
    # CredencialImpresa = Column(Boolean)
    # Entragada = Column(Boolean)
    
    
    def set_FechaNacimiento(self, value):
        if isinstance(value, str):
            self.FechaNacimiento = datetime.strptime(value, '%Y-%m-%d').date()
        else:
            self.FechaNacimiento = value

    def set_FechaAlta(self, value):
        if isinstance(value, str):
            self.FechaAlta = datetime.strptime(value, '%Y-%m-%d').date()
        else:
            self.FechaAlta = value


