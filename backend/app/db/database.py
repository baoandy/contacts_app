from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/contactsdb")

engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(no_cache: bool = False):
    db = SessionLocal()
    if no_cache:
        db.execute("SET LOCAL statement_cache_mode = 'disable'")
    try:
        yield db
    finally:
        db.close() 