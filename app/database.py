from sqlalchemy import create_engine
from dotenv import  load_dotenv
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

load_dotenv()



DB_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engin = create_engine(
    DB_URL,
    echo= True  
)

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engin)

class Base(DeclarativeBase):
    pass

def get_db():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
