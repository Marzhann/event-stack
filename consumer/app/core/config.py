from dotenv import load_dotenv
load_dotenv()

import os

DATABASE_URL=os.getenv("DATABASE_URL", "postgresql+psycopg2://app:app@192.168.20.43:5432/appdb")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
