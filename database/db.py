import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, TIMESTAMP, text
from sqlalchemy_utils import database_exists, create_database

# Configurar logging
timestamp = "%d/%m/%Y %I:%M:%S %p"
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt=timestamp)

# Cargar variables de entorno
def load_env_vars():
    load_dotenv("./env/.env")

    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT")
    database = os.getenv("PG_DATABASE")


    missing = [k for k, v in {
        'PG_USER': user, 'PG_PASSWORD': password,
        'PG_HOST': host, 'PG_PORT': port,
        'PG_DATABASE': database
    }.items() if not v]
    if missing:
        raise EnvironmentError(f"Faltan variables de entorno: {', '.join(missing)}")
    return user, password, host, port, database

user, password, host, port, database = load_env_vars()

database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Crear motor y base de datos si no existe
def creating_engine():
    engine = create_engine(database_url)
    if not database_exists(engine.url):
        create_database(engine.url)
        logging.info(f"Base de datos '{database}' creada exitosamente.")
    else:
        logging.info(f"La base de datos '{database}' ya existe.")
    logging.info("Engine listo para conexiones.")
    return engine

# Inicializar engine y metadata
engine = creating_engine()
metadata = MetaData()

# Definir tabla 'happiness'
happiness = Table(
    'predicted_happiness', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('region', String,  nullable=False),
    Column('happiness_score', Float, nullable=False),
    Column('economy', Float, nullable=True),
    Column('family', Float, nullable=True),
    Column('health', Float, nullable=True),
    Column('freedom', Float, nullable=True),
    Column('government_corruption', Float, nullable=True),
    Column('generosity', Float, nullable=True),
    Column('year', Integer, nullable=False),
    Column('predicted_happiness_score', Float, nullable=False)
)
# Funciones de esquema e inserción
def setup_schema():
    """Verifica o crea el esquema de la tabla 'happiness'."""
    metadata.create_all(engine)
    logging.info("Esquema verificado/creado: 'happiness'.")


def insert_happiness(record: dict):
    """Inserta un registro en la tabla 'happiness', casteando tipos y confirmando la transacción."""
    setup_schema()

    # 1) Convertir strings numéricos a los tipos correctos
    float_fields = [
        'happiness_score', 'economy', 'family',
        'health', 'freedom', 'government_corruption',
        'generosity', 'predicted_happiness_score'
    ]
    for fld in float_fields:
        if fld in record:
            record[fld] = float(record[fld])
    if 'year' in record:
        record['year'] = int(record['year'])

    # 2) Abrir una transacción automática con engine.begin()
    with engine.begin() as conn:
        try:
            result = conn.execute(happiness.insert().values(**record))
            logging.info(f"✅ Registro insertado con id {result.inserted_primary_key}")
        except Exception as e:
            logging.exception(f"❌ Error al insertar registro: {e}")


def fetch_all() -> list[dict]:
    """Recupera todos los registros de 'happiness'."""
    setup_schema()
    with engine.connect() as conn:
        try:
            result = conn.execute(happiness.select())
            rows = [dict(row) for row in result]
            logging.info(f"Recuperados {len(rows)} registros.")
            return rows
        except Exception as e:
            logging.exception(f"Error al recuperar datos: {e}")
            return []

if __name__ == '__main__':
    setup_schema()
    logging.info("db.py ejecutado correctamente.")