from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response
from app.database import db_dep
from app.model import User
from app.utils import verify_password
from app.config import settings
from sqlalchemy import select, delete
from app.schemas import UserLoginRequest, RefreshTokenRequest, UserListResponse
from app.utils import generate_jwt_token, decode_jwt_token
from app.dependense import current_user_jwt_dep

router = APIRouter(prefix="/jwt", tags=["Auth"])


@router.post("/login")
async def jwt_login(session: db_dep, data: UserLoginRequest):
    stmt = select(User).where(User.email == data.email)
    user = (session.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_toke, refresh_token = generate_jwt_token(user.id)

    return {"access_token": access_toke, "refresh_token": refresh_token}


@router.post("/update_access_token")
async def update_refresh_or_access_token(session: db_dep, data: RefreshTokenRequest):
    catch_refresh_token = decode_jwt_token(data.refresh_token)
    exp_time = datetime.fromtimestamp(catch_refresh_token["exp"], tz=timezone.utc)

    if exp_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="refresh token expires")

    user_id = catch_refresh_token["sub"]
    new_access_token = generate_jwt_token(user_id, only_access=True)

    return {"access_token": new_access_token}


@router.get("profile", response_model=UserListResponse)
async def get_profile(current_user: current_user_jwt_dep):
    return current_user
