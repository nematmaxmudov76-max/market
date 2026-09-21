from fastapi import Request, APIRouter, HTTPException, Depends
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from app.model import Category
from app.database import db_dep


router = APIRouter(prefix="/category", tags=["Category"])
