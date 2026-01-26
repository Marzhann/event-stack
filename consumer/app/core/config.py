from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL=os.getenv("DATABASE_URL")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINTS", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")
