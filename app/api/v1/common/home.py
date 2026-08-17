from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.database import db_dep



router = APIRouter(prefix="/home", tags=["Home"])

"""
TODO
1* top mahsulotlar -> eng ko'p sotilayotgan mahsulotlar
2* chegirmadagi productlar
3* user like bosgan productlar
4* 

"""



@router.get("")