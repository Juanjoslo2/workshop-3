import os
import csv
import json
import logging
import time
from kafka import KafkaProducer

# Configurar logging
timestamp = "%d/%m/%Y %I:%M:%S %p"
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt=timestamp)
logger = logging.getLogger(__name__)

TOPIC = 'happiness-transformed'
CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    '..', 'data', 'transform_data', 'transform_happiness_score.csv'
)


def create_producer(max_retries=5, retry_interval=5):
    """Intenta conectar al broker de Kafka varias veces."""
    for attempt in range(1, max_retries + 1):
        try:
            
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                max_in_flight_requests_per_connection=1
            )
            logger.info("Producer conectado a Kafka.")
            return producer
        except Exception as e:
            logger.warning(f"Error conexión Kafka (intento {attempt}/{max_retries}): {e}")
            time.sleep(retry_interval)
    raise RuntimeError("No se pudo conectar al broker de Kafka tras múltiples intentos.")


def load_data() -> list[dict]:
    """Carga las filas del CSV como lista de diccionarios."""
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    logger.info(f"Datos cargados: {len(data)} registros.")
    return data


def send_messages(producer: KafkaProducer, rows: list[dict], batch_size=50):
    """Envía mensajes en lote con confirmación síncrona."""
    count = 0
    for row in rows:
        try:
            future = producer.send(TOPIC, row)
            # Esperar confirmación de envío
            future.get(timeout=10)
            count += 1
            if count % batch_size == 0:
                producer.flush()
                logger.info(f"Enviados {count} mensajes hasta ahora.")
        except Exception as e:
            logger.error(f"Error envío msg #{count + 1}: {e}")
    producer.flush()
    logger.info(f"Envío completado: {count} mensajes enviados a '{TOPIC}'.")


def main():
    rows = load_data()
    producer = create_producer()
    send_messages(producer, rows)
    producer.close()

if __name__ == '__main__':
    main()