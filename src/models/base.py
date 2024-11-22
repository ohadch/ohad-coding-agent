from sqlalchemy.ext.declarative import declarative_base

from src.database import SessionLocal

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()