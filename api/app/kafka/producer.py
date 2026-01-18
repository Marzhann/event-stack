from kafka import KafkaProducer

from app.core.config import KAFKA_BOOTSTRAP_SERVERS


def create_kafka_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        # value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        retries=5,
        linger_ms=10,
    )
