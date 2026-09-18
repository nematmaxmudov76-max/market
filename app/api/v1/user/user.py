from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select
from app.model import User, User_Address
from app.model import Region, Like, Product
from app.schemas import (
    UserListResponse,
    UserCreateRequest,
    UserAddressListResponse,
    CreateUserLikeRequest,
)

from app.utils import hash_password
from app.database import db_dep
from typing import Annotated, Literal

router = APIRouter(prefix="/user", tags=["User"])


# query paramda list ko'rinishida bizga malumot yetib keladi
# TODO Tizimdagi barcha faol foydalanuvchilarning ismi, familiyasi hamda elektron pochta manzilini oling.


# /user_id?q=is_active=<bool>
@router.get("/{user_id}", response_model=UserListResponse)
async def get_users(session: db_dep, user_id: int, is_active: bool = Query(True)):
    stmt = (
        select(User)
        .where(User.is_active == is_active, User.id == user_id)
        .order_by(User.created_at.desc())
    )
    # if is_active is None:
    #     raise HTTPException(status_code=404, detail="user not found")

    res = (session.execute(stmt)).scalars().first()

    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    return res


# TODO Muayyan bir foydalanuvchi (masalan, ID si 5 ga teng bo'lgan) uchun uning profilda saqlab qo'yilgan barcha yetkazib berish manzillarini ko'rsating.
# path param
@router.get("/get_user_address/{user_id}", response_model=UserAddressListResponse)
async def get_user_address(session: db_dep, user_id: int):
    stmt = (
        select(User_Address)
        .where(User_Address.user_id == user_id)
        .options(joinedload(User_Address.region).joinedload(Region.country))
    )
    res = (session.execute(stmt)).scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="user address not found")

    return res


@router.post("/create/like")
async def create_like(session: db_dep, data: CreateUserLikeRequest):
    user = session.get(User, data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    product = session.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    like = Like(user_id=data.user_id, product_id=data.product_id)
    session.add(like)
    session.commit()
    session.refresh(like)

    return like


@router.delete("/delete-user/{user_id}")
async def delete_user(session: db_dep, user_id: int):
    stmt = select(User).where(User.id == user_id)
    res = (session.execute(stmt)).scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    session.delete(res)
    session.flush()
    session.commit()

    return f"user id:{user_id} is deleted"


@router.get("/get_users", response_model=list[UserListResponse])
async def get_active_users(session: db_dep, is_active: bool):
    stmt = select(User).where(User.is_active == is_active)
    res = (session.execute(stmt)).scalars().all()
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return res
