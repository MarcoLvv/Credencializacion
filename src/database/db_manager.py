import email

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from src.config.database_config import Base, engine
from src.models.credencial_model import TbcUsuarios, TbcUsuariosModel
from src.utils.config_manager import get_module_id


def init_db():
    Base.metadata.create_all(bind=engine)
    #print("Tablas creadas.")


class DBManager:
    def __init__(self):
        self.engine = engine
        #Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    def get_next_consecutive(self):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar() + 1
            return f"{count:05d}"

    def get_last(self):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar()
            return f"{count:05d}"

    def generar_folio(self):
        now = datetime.now()
        año = now.strftime("%Y")
        mes = now.strftime("%m")
        modulo = get_module_id()
        consecutivo = self.get_next_consecutive()
        return f"FAMC-{año}{mes}-{modulo}-{consecutivo}"

    def actualizar_ruta_foto(self, folio, nueva_ruta):
        with self.Session() as session:
            credencial = session.query(TbcUsuarios).filter_by(FolioId=folio).first()
            if credencial:
                credencial.RutaFoto = nueva_ruta
                session.commit()
                return True
            return False
   #insertar Credenciales para pruebas
    def insertar_credencial_prueba(self, nombre, curp, ruta_foto):
        folio = self.generar_folio()
        nueva_credencial = TbcUsuarios(
            FolioId=folio,
            Nombre=nombre,
            CURP=curp,
            RutaFoto=ruta_foto
        )
        with self.Session() as session:
            session.add(nueva_credencial)
            session.commit()
        return folio

    def insertar_credencial(self, **datos):
        folio = self.generar_folio()
        nueva_credencial = TbcUsuarios(
            FolioId=folio,
            Nombre=datos.get("Nombre", ""),
            Paterno=datos.get("Paterno", ""),
            Materno=datos.get("Materno", ""),
            CURP=datos.get("CURP", ""),
            Calle=datos.get("Calle", ""),
            Lote=datos.get("Lote", ""),
            Manzana=datos.get("Manzana", ""),
            NumExterior=datos.get("NumExterior", ""),
            NumInterior=datos.get("NumInterior", ""),
            Colonia=datos.get("Colonia", ""),
            CodigoPostal=datos.get("CodigoPostal", ""),
            Municipio=datos.get("Municipio", ""),
            SeccionElectoral=datos.get("SeccionElectoral", ""),
            GeneroId=datos.get("GeneroId", ""),
            Celular=datos.get("Celular", ""),
            Email=datos.get("Email", ""),
            RutaFoto=datos.get("ruta_foto", ""),
            RutaFirma=datos.get("ruta_firma", ""),
            RutaQR=datos.get("ruta_qr", "")
        )
        with self.Session() as session:
            session.add(nueva_credencial)
            session.commit()
        return folio

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

    def actualizar_credencial(self, folio, **datos_actualizados):
        try:
            with self.Session() as session:
                credencial = session.query(TbcUsuarios).filter_by(FolioId=folio).first()
                if not credencial:
                    print(f"[ERROR] No se encontró la credencial con folio: {folio}")
                    return False

                # Asignación dinámica de campos actualizados
                for campo, valor in datos_actualizados.items():
                    if hasattr(credencial, campo):
                        setattr(credencial, campo, valor)

                session.commit()
                print(f"[OK] Credencial actualizada correctamente con folio {folio}")
                return True
        except Exception as e:
            print(f"[ERROR] No se pudo actualizar la credencial: {e}")
            return False


    def eliminar_credencial(self, id_credencial):
        with self.Session() as session:
            credencial = session.query(TbcUsuarios).filter_by(Id=id_credencial).first()
            if credencial:
                session.delete(credencial)
                session.commit()
                return True
            return False
