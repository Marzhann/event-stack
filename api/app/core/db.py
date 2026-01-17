from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.app.core.config import DATABASE_URL


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Dependency for Fast api, temporary keep here
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
