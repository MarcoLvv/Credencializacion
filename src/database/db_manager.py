from datetime import datetime

from sqlalchemy import func
from src.config.database_config import Base, engine, SessionLocal
from src.models.credencial_model import TbcUsuarios
from src.utils.config_manager import get_module_id
from src.utils.data_utils import convert_dates_in_dict


class DBManager:
    def __init__(self):

        self.engine = engine
        self.Session = SessionLocal

    def crear_tablas(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.Session()

    # def cambiar_base(self, nueva_ruta):
    #     nueva_ruta = Path(nueva_ruta)  # Asegurar que es Path
    #     if not nueva_ruta.exists():
    #         print(f"[DBManager] ⚠️ La ruta {nueva_ruta} no existe. ¿Deseas crear una nueva base?")
    #         crear_base_de_datos(nueva_ruta)
    #
    #     self.ruta_db = nueva_ruta
    #     self.engine = create_engine(f"sqlite:///{str(self.ruta_db)}")  # 👈 Conversión importante
    #     self.Session = sessionmaker(bind=self.engine)

    # def crear_base_nueva(self, nombre_archivo):
    #     """
    #     Crea una nueva base con el nombre proporcionado dentro de /data/bases
    #     """
    #     ruta = get_data_db_dir() / f"{nombre_archivo}.db"
    #     if ruta.exists():
    #         print(f"[DBManager] ⚠️ La base {ruta.name} ya existe.")
    #         return False
    #     crear_base_de_datos(ruta)
    #     self.cambiar_base(ruta)
    #     print(f"[DBManager] ✅ Nueva base creada y activada: {ruta.name}")
    #    return True

    def get_last(self):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar() or 0
            return f"{count:05d}"

    def get_next_consecutive(self, offset=0):
        with self.Session() as session:
            count = session.query(func.count(TbcUsuarios.Id)).scalar() or 0
            return f"{count + 1 + offset:05d}"

    def generate_folio(self, consecutivo_directo=None):
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        modulo = get_module_id()

        if consecutivo_directo is None:
            with self.Session() as session:
                count = session.query(func.count(TbcUsuarios.Id)).scalar() or 0
                consecutivo = count + 1
        else:
            consecutivo = consecutivo_directo

        return f"FAMC-{year}{month}-{modulo}-{consecutivo:05d}"

    def insertar_credencial(self, **datos):
        folio = self.generate_folio()
        credential = TbcUsuarios(
            FolioId=folio,
            Nombre=datos.get("Nombre", ""),
            Paterno=datos.get("Paterno", ""),
            Materno=datos.get("Materno", ""),
            CURP=datos.get("CURP", ""),
            FechaNacimiento=datos.get("FechaNacimiento"),
            FechaAlta=datos.get("FechaAlta"),
            Calle=datos.get("Calle", ""),
            Lote=datos.get("Lote", ""),
            Manzana=datos.get("Manzana", ""),
            NumExterior=datos.get("NumExterior", ""),
            NumInterior=datos.get("NumInterior", ""),
            Colonia=datos.get("Colonia", ""),
            CodigoPostal=datos.get("CodigoPostal", ""),
            Municipio=datos.get("Municipio", ""),
            Entidad=datos.get("Entidad", ""),
            SeccionElectoral=datos.get("SeccionElectoral"),
            Genero=datos.get("Genero", ""),
            Celular=datos.get("Celular", ""),
            Email=datos.get("Email", ""),
            RutaFoto=datos.get("RutaFoto", ""),
            RutaFirma=datos.get("RutaFirma", ""),
        )

        with self.Session() as session:
            session.add(credential)
            session.commit()
        return folio

    def insertar_multiples(self, lista_credenciales):
        try:
            with self.Session() as session:
                session.add_all(lista_credenciales)
                session.commit()
            print(f"✅ Insertados {len(lista_credenciales)} usuarios correctamente.")
        except Exception as e:
            print(f"❌ Error al insertar múltiples usuarios: {e}")

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

            # Convertir las fechas en datos_actualizados antes del update
            date_fields = ["FechaAlta", "FechaNacimiento"]
            convert_dates_in_dict(datos_actualizados, date_fields)

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

    def get_credential_by_folio(self, folio_id: str) -> dict:
        session = self.Session()
        try:
            user = session.query(TbcUsuarios).filter_by(FolioId=folio_id).first()
            if user:
                return user.__dict__
            return None

        finally:
            session.close()

    def obtener_credencial(self):
        with self.Session() as session:
            return session.query(TbcUsuarios)

    def update(self, usuario):
        with self.Session() as session:
            session.merge(usuario)
            session.commit()

    def incrementar_veces_impresa(self, folio_id: str):
        """Incrementa el contador de VecesImpresa en 1 para una credencial."""
        session = self.Session()
        try:
            credencial = session.query(TbcUsuarios).filter_by(FolioId=folio_id).first()
            if credencial:
                credencial.VecesImpresa = (credencial.VecesImpresa or 0) + 1
                session.commit()
        except Exception as e:
            print(f"Error al incrementar VecesImpresa para {folio_id}: {e}")
            session.rollback()
