import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings, IS_VERCEL

# Agar DATABASE_URL yoki Postgres sozlamalari berilgan bo'lsa Postgres ishlaydi,
# aks holda vaqtinchalik/Vercel test rejimi uchun SQLite ishlatiladi.
if settings.DATABASE_URL:
    DB_URL = settings.DATABASE_URL
elif settings.DB_HOST and settings.DB_USER and settings.DB_NAME:
    DB_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
else:
    sqlite_path = "/tmp/market.db" if IS_VERCEL else "./market_temp.db"
    DB_URL = f"sqlite:///{sqlite_path}"

engine_kwargs = {"echo": False}
if DB_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DB_URL, **engine_kwargs)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Session uchun FastAPI dependency
db_dep = Annotated[Session, Depends(get_db)]
