from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func, exists
from sqlalchemy.orm import joinedload, selectinload, join, outerjoin
from app.database import db_dep
from app.model import (
    Product,
    Category,
    Discount,
    User_Rating,
    Shop_Product,
    Comment,
    Product_Media,
    Like,
)


router = APIRouter(prefix="/product", tags=["Product"])

"""
ONE PRODUCT DETAIL => views -> PASSIVE, ACTIVE USERS

3 types query will build:
1)product detail
2)about shop
3)this types products
"""

# TODO 1* name, descriptions, price, current_quantity, size,
@router.get("/details/{product_id}", response_model=)
async def get_product_details(session: db_dep, product_id: int, current_user:int):
    is_liked_product = (
        exists()
        .where(
            Like.product_id == Product.id,
            Like.user_id == current_user
        )
        .collate(Product)
        if current_user else False
        )

    stmt = (
        select(
            #avg reting, reting count 
            func.coalesce(
                func.avg(User_Rating.ball),
                0.0
            )
            .label("product rating avg"),
            func.coalesce(
                func.count(User_Rating.id),
                0
            )
            .label("product rating counts"),

            Product_Media.media_id,
            Product.name,
            Product.description,
            func.coalesce(Product.size, None).label("product size"),
            Product.category_id,

            # comment faqat zakas qilib va is_active=true bo'lganlar kelsin!!
            func.coalesce(Comment.title if Comment.is_active == True else None, None ).label("users comments"),

            #product current_cuantity
            func.coalesce(Product.current_quantity, 0).label("product current count in store"),

            # current prise
            func.coalesce(
                Product.price - Product.price*(int(Discount.percent))/100 if Discount.is_active else Product.price
            ).label("current prise"),

            # discount title
            func.coalesce(Discount.title, Discount.category, None).label("discount title"),

            #expiretion date
            is_liked_product
        )
        .where(Product.is_active == True, Product.id == product_id)
        # user_rating, product_media, category, comment, discount,
        .join(Product.id == User_Rating.product_id)
        .join(Product.id == Product_Media.product_id)
        .join(Product.category_id == Category.id)
        .outerjoin(Product, Product.id == Comment.product_id)
        .join(Product.discount_id == Discount.id)
    )
    one_product = (session.execute(stmt)).mappings()

    if not one_product:
        raise HTTPException(status_code=404, detail="product not found")

    return one_product