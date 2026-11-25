import time
import logging
import redis
import smtplib
from enum import Enum
from datetime import datetime, timezone, timedelta

from email.mime.text import MIMEText
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.config import settings

logger = logging.getLogger("uvicorn.error")


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


def send_email(to_email: str, subject: str, body: str):
    if not settings.EMAIL_PASSWORD:
        logger.warning(f"[DEMO MODE - SMTP yo'q] Email -> {to_email} | {subject}: {body}")
        return
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to_email

    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
        server.send_message(msg)


class _InMemoryRedis:
    """Redis bo'lmagan muhit (masalan Vercel demo) uchun vaqtinchalik xotira kesh."""

    def __init__(self):
        self._store: dict[str, tuple[bytes, float | None]] = {}

    def setex(self, name: str, time_sec: int, value: str | bytes):
        raw = value.encode("utf-8") if isinstance(value, str) else value
        self._store[name] = (raw, time.time() + int(time_sec))

    def get(self, name: str) -> bytes | None:
        item = self._store.get(name)
        if not item:
            return None
        raw, exp = item
        if exp is not None and time.time() > exp:
            self._store.pop(name, None)
            return None
        return raw

    def delete(self, *names: str) -> int:
        deleted = 0
        for name in names:
            if name in self._store:
                del self._store[name]
                deleted += 1
        return deleted


class _FallbackRedis:
    """Avval haqiqiy Redis ga ulanadi; ulanmasa yoki REDIS_URL bo'sh bo'lsa InMemory ga o'tadi."""

    def __init__(self, url: str):
        self._memory = _InMemoryRedis()
        self._client = None
        if url and url.startswith(("redis://", "rediss://", "unix://")):
            try:
                client = redis.from_url(url, socket_connect_timeout=1)
                client.ping()
                self._client = client
            except Exception as exc:
                logger.warning(f"Redis ulanmadi ({exc}), vaqtinchalik InMemory rejim yoqildi.")

    def setex(self, name: str, time_sec: int, value: str | bytes):
        if self._client is not None:
            try:
                return self._client.setex(name, time_sec, value)
            except Exception:
                pass
        return self._memory.setex(name, time_sec, value)

    def get(self, name: str):
        if self._client is not None:
            try:
                return self._client.get(name)
            except Exception:
                pass
        return self._memory.get(name)

    def delete(self, *names: str):
        if self._client is not None:
            try:
                return self._client.delete(*names)
            except Exception:
                pass
        return self._memory.delete(*names)


redis_url = _FallbackRedis(settings.REDIS_URL)


#### ENUMS ________________________________________________________________________________-
class Target(Enum):
    WEEK = "weekly"
    MONTH = "monthly"


class ManageNotificationCreate(Enum):
    SINGLE = "single"
    ALL = "all"
    ACTIVE_USER = "active_users"
    MERCHANTS = "merchants"
    COURIERS = "couriers"
    MANAGERS = "managers"


class ChooseRoleRequest(str, Enum):
    MERCHANT = "merchant"
    COURIER = "courier"
    MANAGER = "manager"
    ADMIN = "admin"


class RoleRequestStatus(str, Enum):
    PENDING = "pending"  # user aplicationni send qilingandagi va admin tomonidan ko'rib chiqilish vaqti
    WAITING = "waiting"  # admin ko'rib chiqdi va register(email/sms) qilish uchun ochiq
    APPROVED = "approved"  # user login qilish uchun ochiq
    REJECTED = "rejected"  # raq qilindi
    COMPLETED = "completed"  # to'liq login qilingandan keyingi status
