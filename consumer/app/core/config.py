from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL=os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@192.168.20.43:5432/appdb")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINTS", "http://192.168.20.43:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
