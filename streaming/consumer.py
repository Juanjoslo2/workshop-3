import logging
from json import loads
import joblib
import os
import sys
import pandas as pd
from kafka import KafkaConsumer

# permitir import desde nivel raíz
dir_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(dir_raiz)

# Importar funciones de la capa de BD
from database.db import setup_schema, insert_happiness

# Configurar logging
timestamp = "%d/%m/%Y %I:%M:%S %p"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt=timestamp
)
logger = logging.getLogger(__name__)

# Verificar/crear esquema de BD
setup_schema()
logger.info("Esquema de BD verificado/creado.")

# Ruta al pipeline completo
pipeline_path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'data', 'model',
    'best_model_xgboost_pipeline.pkl'
)

if not os.path.exists(pipeline_path):
    logger.error(f"No existe el pipeline en: {pipeline_path}")
    sys.exit(1)

pipeline = joblib.load(pipeline_path)
logger.info(f"Pipeline cargado desde: {pipeline_path}")

# Inicializar consumidor Kafka
consumer = KafkaConsumer(
    'happiness-transformed',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda m: loads(m.decode('utf-8'))
)
logger.info("Conectado a Kafka topic: 'happiness-transformed'.")

# Bucle principal: leer, predecir e insertar en BD
for mensaje in consumer:
    registro = mensaje.value.copy()
    # Quitar campos que no necesita el modelo
    registro.pop('country', None)

    try:
        X_df = pd.DataFrame([registro])
        pred = pipeline.predict(X_df)[0]
        registro['predicted_happiness_score'] = float(pred)
        insert_happiness(registro)
        logger.info(f"Registro insertado con predicción: {registro}")
    except Exception as e:
        logger.error(f"Error procesando mensaje: {e}")
