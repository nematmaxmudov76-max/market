from datetime import datetime, timezone, timedelta

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import select
from app.database import db_dep
from typing import Annotated
from app.utils import verify_password, decode_jwt_token, Target
from app.model import (
    User,
    UserSessionToken,
    Product,
)
from app.config import settings
from enum import Enum

# BASIC AUTH
basic = HTTPBasic()
basic_auth = Annotated[HTTPBasicCredentials, Depends(basic)]

# JWT AUTH
jwt_securty = HTTPBearer(auto_error=False)


router = APIRouter(prefix="/basic_auth", tags=["Auth"])


# for basic auth
def get_current_user_basic(session: db_dep, credention: basic_auth):
    stmt = select(User).where(User.email == credention.username)
    res = (session.execute(stmt)).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(credention.password, res.password_hash):
        raise HTTPException(status_code=401, detail="incorrect password")

    return res


current_user_basic = Annotated[User, Depends(get_current_user_basic)]


# for session auth


def check_current_user_session(session: db_dep, request: Request) -> dict:
    token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="not authenticate")

    stmt = select(UserSessionToken).where(UserSessionToken.token == token)
    user_obj = (session.execute(stmt)).scalars().first()

    if not user_obj:
        raise HTTPException(status_code=401, detail="not authenticate")

    if user_obj.expires_at < datetime.now(tz=timezone.utc):
        session.delete(user_obj)
        session.commit()
        raise HTTPException(status_code=401, detail="time expired, login again")

    stmt = select(User).where(User.id == user_obj.user_id)
    user = (session.execute(stmt)).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="user not found")

    return {"check": True, "user_id": User.id}


check_user_session_dep = Annotated[dict, Depends(check_current_user_session)]


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


async def get_current_user_login(request: Request) -> User:
    user: User | None = getattr(request.state, "user_login", None)

    if user is None:
        raise HTTPException(status_code=401, detail="user not found or session expired")
    return user


current_user_dep = Annotated[User, Depends(get_current_user_login)]


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


