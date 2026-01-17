from dotenv import load_dotenv
load_dotenv()

import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if SECRET_KEY is None:
    print("WARNING: SECRET_KEY is NULL")

DATABASE_URL=os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@192.168.20.43:5432/appdb")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKER = os.getenv("S3_BUCKET", "event-bucket")
S3_REGION = os.getenv("S3_REGION", "us-east-1")