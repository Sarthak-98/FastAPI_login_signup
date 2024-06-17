from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr,declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()