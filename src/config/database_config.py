from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from src.utils.rutas import get_bd_path

DB_PATH = get_bd_path() / "credenciales.db"
engine = create_engine(f'sqlite:///{DB_PATH}')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()