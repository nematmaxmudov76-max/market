from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import  joinedload, selectinload
from sqlalchemy import select
from app.model import User , User_Address
from app.model import Region, Country
from app.schemas.user import (
    UserListResponse, 
    UserCreateRequest,
    UserAddressListResponse,
)

from app.database import db_dep
from pydantic import BaseModel, Field
from typing import Annotated, Literal

router = APIRouter(prefix="/profil", tags=["User"])


@router.post("/create")
async def create_user(session:db_dep, data:UserCreateRequest):
    users = User(
        id = data.id,
        first_name = data.first_name,
        last_name = data.last_name,
        age = data.age,
        email = data.email,
        tell_number = data.tell_number,
        password = data.password,
        password_hash = data.password_hash,
        is_active = data.is_active, 
    )
    session.add(users)
    session.commit()
    session.refresh(users)

    return users

# query paramda list ko'rinishida bizga malumot yetib keladi
# TODO Tizimdagi barcha faol foydalanuvchilarning ismi, familiyasi hamda elektron pochta manzilini oling.

@router.get("/{user_id}", response_model=list[UserListResponse])
async def get_users(session:db_dep, is_active:bool | None = None,):
    stmt = (
    select(User)
    .where(User.is_active == is_active)
    .order_by(User.created_at.desc())
    )
    if is_active is  None:
        raise HTTPException(status_code=404, detail="user not found")
    
    res = session.execute(stmt)
    return res.scalars().all()

# TODO Muayyan bir foydalanuvchi (masalan, ID si 5 ga teng bo'lgan) uchun uning profilda saqlab qo'yilgan barcha yetkazib berish manzillarini ko'rsating.

@router.get("/get_user_address/{user_id}", response_model=UserAddressListResponse) 
async def get_user_address(session:db_dep, user_id:int):
    stmt = (
        select(User_Address)
        .where(User_Address.user_id == user_id)
        .order_by(User_Address.id.desc())
        .options(
            joinedload(User_Address.region).joinedload(Region.country)
            )
        
    )
    res = (session.execute(stmt)).scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="user address not found")
        
    return res
    

    
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@router.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query