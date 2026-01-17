from dotenv import load_dotenv
load_dotenv("app/.env")

from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.app.kafka.producer import create_kafka_producer
from api.app.api.v1.routes.orders import router as orders_router
from api.app.api.v1.routes.users import router as user_router
from api.app.auth.router import router as auth_router

# one time run, remove after
# from api.app.core.db import Base, engine
# print("DB URL:", str(engine.url))
# print("SQLAlchemy models registered:", sorted(Base.metadata.tables.keys()))
# Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    # -- Startup --
    producer = create_kafka_producer()
    app_.state.kafka_producer = producer
    print("Kafka producer connected!")

    yield

    # -- Shutdown --
    print("Shutting down Kafka producer...")
    producer.flush()
    producer.close()
    print("Kafka producer closed.")


app = FastAPI(lifespan=lifespan)

app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_router, prefix="/auth/router", tags=["auth"])


@app.get("/health")
def health():
    return {"status": "ok"}