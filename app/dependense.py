from datetime import datetime, timezone, timedelta

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import db_dep, get_db
from typing import Annotated
from app.utils import verify_password, decode_jwt_token, Target
from app.model import (
    User,
    UserSessionToken,
    Product,
)
from app.config import (
    settings,
    INCLUDE_PATH_COURIERS,

)
from enum import Enum


# JWT AUTH
jwt_securty = HTTPBearer(auto_error=False)


router = APIRouter(prefix="/basic_auth", tags=["Auth"])




# Role base control for merchant, courier, manager, admin


#logins user
def get_current_login_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = getattr(request.state, "user", None)
    if user is None:
        raise HTTPException(status_code=401, detail="Tizimga kiring")

    user_id = user.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token noto'g'ri")

    user_obj = db.get(User, int(user_id))
    if user_obj is None or user_obj.is_deleted or not user_obj.is_active:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi yoki faol emas")

    return user_obj

#couriers
def get_current_courier_user(user: User = Depends(get_current_login_user)) -> User:
    if not user.is_courier:
        raise HTTPException(status_code=403, detail="only couriers")
    return user


# merchants
def get_current_merchant_user(user:User = Depends(get_current_login_user)):

    if not user.is_merchant:
        raise HTTPException(status_code=403, detail="only for merchants")
    return user

#managers
def get_current_manager_user(user: User = Depends(get_current_login_user)):

    if not user.is_manager:
        raise HTTPException(status_code=403, detail="only managers")

    return user


#admins
def get_current_admin_user(user: User = Depends(get_current_login_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="only admins")
    return user



current_user_dep = Annotated[User, Depends(get_current_login_user)]
current_courier_dep = Annotated[User, Depends(get_current_courier_user)]
current_admin_dep = Annotated[User, Depends(get_current_admin_user)]
current_merchant_dep = Annotated[User, Depends(get_current_merchant_user)]
currnet_manager_user_dep = Annotated[User, Depends(get_current_manager_user)]


"""
active / passive userlarni argumentga kiruvchi user_id bilan teshkirilari
state dan url ni olib unga mos bo'lgan path ga ruxsat beriladi
"""







# home page dependency

def get_pagination(min: int = 0, max: int = settings.MAX_LIKED_PRODUCT) -> dict:
    return {"min": min, "max": max}


def current_discount_date(target_data: Target = Target.WEEK):
    days = 7 if target_data == Target.WEEK else 30
    return datetime.now() - timedelta(days=days)


def get_current_product(session: db_dep, request: Request, product_id: int):
    stmt = select(Product).where(Product.id == product_id, Product.is_active == True)
    product = (session.execute(stmt)).scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    return {"product_id":product_id} 

current_product_dep = Annotated[dict, Depends(get_current_product)]









def get_current_user_jwt(
    session: db_dep, credential: HTTPAuthorizationCredentials = Depends(jwt_securty)
):
    if not credential:
        raise HTTPException(status_code=401, detail="invalit credetial")

    decode = decode_jwt_token(credential.credentials)
    if not decode or "sub" not in decode or "exp" not in decode:
        raise HTTPException(status_code=401, detail="invalid token")

    user_id = int(decode["sub"])

    exp_time = datetime.fromtimestamp(decode["exp"], tz=timezone.utc)

    if exp_time < datetime.now(tz=timezone.utc):
        raise HTTPException(status_code=401, detail="time expires")

    stmt = select(User).where(User.id == user_id)
    user = (session.execute(stmt)).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="user not found")

    return user


current_user_jwt_dep = Annotated[User, Depends(get_current_user_jwt)]




# async def get_current_courier_user(request: Request) -> User[object] | None:
#     get_user: User | None = getattr(request.state, "user", None)

#     if not get_user or get_user is None:
#         raise HTTPException(status_code=401, detail="user not found or session expired")

    
#     try:
#         user_id = int(get_user.get("sub"))
#         exp_timestamp = get_user.get("exp")

#         if not exp_timestamp:
#             raise HTTPException(status_code=401, detail="time expires")
#         exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
#         if exp_time < datetime.now(tz=timezone.utc):
#             raise HTTPException(status_code=401, detail="time expires")

#         db = next(get_db())
#         try: 
#             current_user = db.query(User).filter(User.id == user_id).first()

#             if (current_user and current_user.is_courier):
#                 return current_user

#         finally:
#             db.close()

#     except Exception:
#         return None

# current_courier_dep = Annotated[User, Depends(get_current_courier_user)]







