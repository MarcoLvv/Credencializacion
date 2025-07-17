from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.rutas import get_bd_path

# DB_PATH = get_bd_path() / "credencialesv2.db"
# engine = create_engine(f'sqlite:///{DB_PATH}')
# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()


Base = declarative_base()

# Variables globales
engine = None
SessionLocal = None

def cambiar_db_path(nueva_ruta):
    global engine, SessionLocal
    engine = create_engine(f"sqlite:///{nueva_ruta}", echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine)

# Inicial por defecto
cambiar_db_path(get_bd_path())