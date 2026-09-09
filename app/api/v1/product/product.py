from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from app.database import db_dep
from app.model import (
    Product,
    Category,
    Discount,
    User_Rating,
    Shop_Product,
)


router = APIRouter(prefix="/product", tags=["Product"])


# TODO 1* name, descriptions, price, current_quantity, size,
@router.get("/details/{product_id}")
async def get_product_details(session: db_dep, product_id: int, is_active: bool):
    stmt = (
        select(Product, func.avg(User_Rating.ball), func.count(Shop_Product.id))
        .outerjoin(User_Rating, User_Rating.product_id == Product.id)
        .join(Shop_Product, Shop_Product.product_id == Product.id)
        .where(Product.id == product_id)
    )


# TODO 2* shu categoryadagi productlar
# @router.get("/category-products")
# async def get_product_in_category(session:db, )
