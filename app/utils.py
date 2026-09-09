from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError
from app.config import settings


context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password_hash: str):
    return context.hash(password_hash)


def verify_password(password_hash: str, password2: str):
    return context.verify(password_hash, password2)


def generate_jwt_token(user_id: int, only_access: bool = False):
    access_token = jwt.encode(
        algorithm=settings.ALGORITHM,
        key=settings.SECRET_KEY,
        claims={
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        },
    )

    # faqat access token kerak bo'lgande
    if only_access:
        return access_token

    refresh_token = jwt.encode(
        algorithm=settings.ALGORITHM,
        key=settings.SECRET_KEY,
        claims={
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        },
    )
    return access_token, refresh_token


def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM,
        )
        return payload
    except JWTError:
        return None
