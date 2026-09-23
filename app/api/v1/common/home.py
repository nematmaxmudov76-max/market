from tempfile import template
from fastapi import APIRouter, HTTPException, Request, Depends
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
from app.middleware import limiter
from app.dependense import (
    get_current_user,
    get_pagination,
    current_discount_date,
)
from typing import Annotated


router = APIRouter(prefix="/home", tags=["Home"])


# ["/user_id?q=is_active=<bool>"] barcha like bosilgan productlar
@limiter.limit("10/minute")
@router.get("/liked-products", response_model=list[ProductListResponse])
async def get_liked_product(
    request: Request,
    session: db_dep,
    current_user: Annotated[User, Depends(get_current_user)],
    pagination: Annotated[dict, Depends(get_pagination)],
):
    stmt = (
        select(Product)
        .join(Like, Like.product_id == Product.id)
        .join(User, User.id == Like.user_id)
        .where(User.is_active == True, Like.user_id == current_user)
        .order_by(Like.created_at.desc())
        .offset(pagination["min"])
        .limit(pagination["max"])
    )

    item = session.execute(stmt)
    res = item.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="liked product not found")

    return res


# (query param) product ni name bo'yicha search qilish
@limiter.limit("15/minute")
@router.get("/search-by-name", response_model=list[ProductListResponse])
async def search_by_name(request: Request, session: db_dep, search: str):
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
async def search_by_category(request: Request, session: db_dep, is_active: bool):
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
async def get_discount_products(
    request: Request,
    session: db_dep,
    pagination: Annotated[dict, Depends(get_pagination)],
):
    stmt = (
        select(Product)
        .join(Discount, Discount.id == Product.discount_id)
        .where(Discount.is_active == True, Product.is_active == True)
        .order_by(Product.id.desc())
        .options(joinedload(Product.discount))
        .offset(pagination["min"])
        .limit(pagination["max"])
    )
    product = session.execute(stmt)
    res = product.scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="product not found")
    return res


"""
(query) -4* oxirgi hafta/oy ichida chegirmaga ega productlar
"""


@limiter.limit("30/minute")
@router.get("/monthly-discount", response_model=list[ProductListResponse])
async def get_monthly_discount(
    request: Request,
    session: db_dep,
    target_layer: Annotated[object, Depends(current_discount_date)],
    pagination: Annotated[dict, Depends(get_pagination)],
):
    stmt = (
        select(Product)
        .join(Discount, Discount.id == Product.discount_id)
        .where(Product.is_active == True, Discount.created_at >= target_layer)
        .group_by(Product.id)
        .order_by(Product.id.desc())
        .options(joinedload(Product.discount))
        .offset(pagination["min"])
        .limit(pagination["max"])
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
async def get_top_10_products(
    request: Request,
    session: db_dep,
    pagination: Annotated[dict, Depends(get_pagination)],
    target_layer: Annotated[object, Depends(current_discount_date)],
):
    stmt = (
        select(Product)
        .join(User_Search, User_Search.product_id == Product.id)
        .outerjoin(
            User_Rating, User_Rating.product_id == Product.id
        )  # oldin ratingi borlari keyin yo'qlari
        .where(Product.is_active == True, User_Search.created_at >= target_layer)
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
async def get_user_top_products(request: Request, session: db_dep, user_id: int):
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


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@router.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
