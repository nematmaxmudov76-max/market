from fastapi import APIRouter, HTTPException
from sqlalchemy import select, func, exists, null, case, and_
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
from app.schemas import OneProductDetailsRespones
from app.dependense import current_product_dep

router = APIRouter(prefix="/product", tags=["Product"])

"""
ONE PRODUCT DETAIL => views -> PASSIVE, ACTIVE USERS

3 types query will build:
1)product detail
2)about shop
3)this types products
"""

# TODO 1* name, descriptions, price, current_quantity, size,
@router.get("/details/{product_id}", response_model=OneProductDetailsRespones)
async def get_product_details(session: db_dep, product: current_product_dep = None):
    product_id = product.get("product_id")
    
    if not product or product is None:
        raise HTTPException(status_code=404, detail="current product not found")
    
    is_liked_product = (
        exists()
        .where(
            Like.product_id == Product.id,
            Like.user_id == current_user
        )
        .correlate(Product)
        if current_user else False
    )

    # 2. Asosiy So'rov (Query)
    stmt = (
        select(
            Product.id.label("id"),
            Product.name.label("name"),
            Product.description.label("description"),
            Product.size.label("product_size"),
            Product.category_id.label("category_id"),
            func.coalesce(Product.current_quantity, 0).label("product_current_count_in_store"),
            
            # Rating
            func.coalesce(func.avg(User_Rating.ball), 0.0).label("product_rating_avg"),
            func.coalesce(func.count(User_Rating.id), 0).label("product_rating_counts"),

            # Media ID (Array or First ID)
            Product_Media.media_id.label("media_id"),

            # Comment (Faqat active bo'lgan birinchi yoki oxirgi comment sarlavhasi)
            func.max(
                case(
                    (Comment.is_active == True, Comment.title),
                    else_=None
                )
            ).label("users_comments"),

            # Discount va Hisoblangan Joriy Narx
            func.coalesce(
                case(
                    (Discount.is_active == True, Product.price - (Product.price * Discount.percent / 100)),
                    else_=Product.price
                ),
                Product.price
            ).label("current_price"),

            case(
                (Discount.is_active == True, func.coalesce(Discount.title, Discount.category)),
                else_=None
            ).label("discount_title"),

            # Is Liked
            is_liked_product.label("is_liked")
        )
        .outerjoin(User_Rating, User_Rating.product_id == Product.id)
        .outerjoin(Product_Media, Product_Media.product_id == Product.id)
        .outerjoin(Category, Category.id == Product.category_id)
        .outerjoin(Comment, and_(Comment.product_id == Product.id, Comment.is_active == True))
        .outerjoin(Discount, Discount.id == Product.discount_id)
        .where(Product.is_active == True, Product.id == product_id)
        .group_by(
            Product.id, 
            Product_Media.media_id, 
            Discount.is_active, 
            Discount.percent, 
            Discount.title, 
            Discount.category
        )
    )

    result = session.execute(stmt).mappings().first()

    if not result:
        raise HTTPException(
            status_code=404, 
            detail="Product not found"
        )

    return result


# @router.get("/shop-about/{}")