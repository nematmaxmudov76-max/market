from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select, func
from sqlalchemy.orm import join
from app.database import db_dep
from app.model import (
    Bucket,
    Bucket_Product,
    Product,
)
from app.dependense import current_active_user_dep, get_current_product

router = APIRouter(prefix="/bucked", tags=["Bucked"])


# #post method orqali productni buckedga qo'shish
# @router.post("/push-product")
# async def push_product_bucked(session:db_dep, )