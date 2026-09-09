import secrets
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy import select, delete
from app.model import UserSessionToken, User
from app.database import db_dep
from app.utils import verify_password
from app.schemas import UserLoginRequest
from app.config import settings
from app.dependense import check_user_session_dep
from app.schemas import UserListResponse


router = APIRouter(prefix="/session", tags=["Auth"])


# register qilingan userni cookiesiga session_id qo'shib berish vaqtinchalik
@router.post("/login")
async def login(session: db_dep, data: UserLoginRequest, response: Response):
    stmt = select(User).where(User.email == data.email)
    user = (session.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    stmt = delete(UserSessionToken).where(UserSessionToken.user_id == user.id)
    session.execute(stmt)
    session.flush()

    token = secrets.token_urlsafe(32)

    new_session = UserSessionToken(
        token=token,
        user_id=user.id,
        expires_at=datetime.now(tz=timezone.utc)
        + timedelta(days=settings.SESSION_EXPIRATION_DAY),
    )
    session.add(new_session)
    session.commit()
    session.refresh(new_session)

    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS
        samesite="strict",
        max_age=settings.SESSION_EXPIRATION_DAY * 24 * 60 * 60,
    )
    return {"token": token}


@router.get("/profil", response_model=UserListResponse)
async def get_user_profile(
    session: db_dep, check: check_user_session_dep, user_id: int
):
    if not check.get("check"):
        raise HTTPException(status_code=404, detail="user not found")
    print(f"Check: >>>>>>>>> {check['check']}")
    stmt = select(User).where(User.id == user_id)
    user = (session.execute(stmt)).scalars().first()

    return user
