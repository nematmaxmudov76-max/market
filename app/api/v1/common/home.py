from tempfile import template

from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from app.database import db_dep
from app.model import (
    Like,
    User,
    Product,
    Category,
    Discount,
    User_Search,
    User_Rating,
)
from datetime import datetime, timedelta
from enum import Enum
from app.schemas import ProductListResponse
from middleware import limiter

router = APIRouter(prefix="/home", tags=["Home"])


# ["/user_id?q=is_active=<bool>"] barcha like bosilgan productlar
@limiter.limit("10/minute")
@router.get("/liked-products", response_model=list[ProductListResponse])
async def get_liked_product(session: db_dep, is_active: bool, user_id: int):
    stmt = (
        select(Product)
        .join(Like, Like.product_id == Product.id)
        .join(User, User.id == Like.user_id)
        .where(User.is_active == is_active, Like.user_id == user_id)
        .order_by(Like.created_at.desc())
    )

    item = session.execute(stmt)
    res = item.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="liked product not found")

    return res


# (query param) product ni name bo'yicha search qilish
@limiter.limit("15/minute")
@router.get("/search-by-name", response_model=list[ProductListResponse])
async def search_by_name(session: db_dep, search: str):
    stmt = (
        select(Product)
        .where(Product.name.like(f"%{search}%"))
        .order_by(Product.id.desc())
    )
    name = session.execute(stmt)
    res = name.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")

    return res


# (query) productni category bo'yicha search qilish
@limiter.limit("20/minute")
@router.get("/search-by-category", response_model=list[ProductListResponse])
async def search_by_category(session: db_dep, is_active: bool):
    stmt = (
        select(Product)
        .join(Category, Category.id == Product.category_id)
        .where(Product.is_active == is_active)
        .order_by(Product.created_at.desc())
        .options(selectinload(Product.category))
    )

    product = session.execute(stmt)
    res = product.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")

    return res


"""
(query) mavsumiy chegirmalar, yani muddati 
tugamagan chegirmalarga ega mahsulotlarni tortib kelish
"""


@router.get("/discount-products", response_model=list[ProductListResponse])
async def get_discount_products(session: db_dep, is_active: bool):
    stmt = (
        select(Product)
        .join(Discount, Discount.id == Product.discount_id)
        .where(Discount.is_active == is_active, Product.is_active == is_active)
        .order_by(Product.id.desc())
        .options(joinedload(Product.discount))
    )
    product = session.execute(stmt)
    res = product.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")
    return res


class Current_date(Enum):
    MONTHLY = "monthly"
    WEEK = "week"


"""
(query) -4* oxirgi hafta/oy ichida chegirmaga ega productlar
"""

@limiter.limit("30/minute")
@router.get("/monthly-discount", response_model=list[ProductListResponse])
async def get_monthly_discount(
    session: db_dep, is_active: bool, month_or_week: Current_date
):
    if month_or_week == Current_date.WEEK:
        current_date = datetime.now() - timedelta(days=7)
    else:
        current_date = datetime.now() - timedelta(days=30)

    stmt = (
        select(Product)
        .join(Discount, Discount.id == Product.discount_id)
        .where(Product.is_active == is_active, Discount.created_at >= current_date)
        .group_by(Product.id)
        .order_by(Product.id.desc())
        .options(joinedload(Product.discount))
    )
    res = (session.execute(stmt)).scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")
    return res


"""
- 5* oxirgi hafta ichida eng ko'p qidiruvdagi va ratingi baland productlar
"""

@limiter.limit("20/minute")
@router.get("/top-10-products", response_model=list[ProductListResponse])
async def get_top_10_products(session: db_dep, is_active: bool):
    last_one_week = datetime.now() - timedelta(days=7)
    stmt = (
        select(Product)
        .join(User_Search, User_Search.product_id == Product.id)
        .outerjoin(
            User_Rating, User_Rating.product_id == Product.id
        )  # oldin ratingi borlari keyin yo'qlari
        .where(Product.is_active == is_active, User_Search.created_at >= last_one_week)
        .group_by(Product.id)
        .order_by(
            func.count(User_Search.user_id).desc(), func.avg(User_Rating.ball).desc()
        )
        .limit(10)
    )
    res = (session.execute(stmt)).scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")

    return res


"""
- 6* user oxirgi hafta ichida eng ko'p qidirgan va ratingi baland productlar
"""

@limiter.limit("10/minute")
@router.get("/user-top-products", response_model=list[ProductListResponse])
async def get_user_top_products(session: db_dep, user_id: int):
    last_one_week = datetime.now() - timedelta(days=7)
    stmt = (
        select(Product)
        .join(User_Search, User_Search.product_id == Product.id)
        .outerjoin(
            User_Rating, User_Rating.product_id == Product.id
        )  # oldin ratingi borlari keyin yo'qlari
        .where(
            Product.is_active == True,
            User_Search.user_id == user_id,
            User_Search.created_at >= last_one_week,
        )
        .group_by(Product.id)
        .order(
            func.count(User_Search.user_id).desc(), func.avg(User_Rating.ball).desc()
        )
        .limit(10)
    )

    res = (session.execute(stmt)).scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")

    return res


