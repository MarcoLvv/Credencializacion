from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.rutas import get_bd_path  # Ruta fija a la base principal

DB_PATH = get_bd_path()  # Siempre retorna la ruta de una única base fija
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
