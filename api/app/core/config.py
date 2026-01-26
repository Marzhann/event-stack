from dotenv import load_dotenv
load_dotenv()

import os


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if SECRET_KEY is None:
    print("WARNING: SECRET_KEY is NULL")

DATABASE_URL=os.getenv("DATABASE_URL")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
