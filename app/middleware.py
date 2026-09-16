import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import get_db  # get_db o'rniga SessionLocal
from app.model import User
from app.utils import decode_jwt_token
from app.config import EXCLUDE_PATHS
from jose import JWTError


class SessionValidationMiddleware(BaseHTTPMiddleware):

  async def dispatch(self, request: Request, call_next):
    request.state.user = None
    path = request.url.path

    # 1. Admin panel, EXCLUDE_PATH ichidagi va ochiq yo'llarni bypass qilish (tekshirmasdan o'tkazish)
    if (
        path.startswith("/admin")
        or path.startswith("/docs")
        or path.startswith("/openapi.json")
        or path.startswith("/redoc")
        or path in EXCLUDE_PATHS
    ):
      return await call_next(request)

    # 2. Authorization Header yoki Cookie'dan tokenni olish
    auth_header = request.headers.get("Authorization")
    token = None
    token_from_cookie = False

    if auth_header and auth_header.startswith("Bearer "):
      token = auth_header.split(" ")[1]
    else:
      token = request.cookies.get("access_token") or request.cookies.get(
          "refresh_token"
      )
      token_from_cookie = token is not None

    # 3. Tokenni dekod qilish va foydalanuvchini bazadan qidirish
    if token:
      db = next(get_db())
      try:
        payload = decode_jwt_token(token)
        if payload:
          user_id = payload.get("sub")
          exp_time = payload.get("exp")

          # Unix timestamp orqali vaqtni tekshirish
          current_timestamp = int(time.time())

          if user_id and exp_time and int(exp_time) > current_timestamp:
            user = (
                db.query(User)
                .filter(User.id == int(user_id), User.is_deleted ==False)
                .first()
            )

            if user:
              request.state.user = user
      except Exception:
        # JWT dekod qilishda yoki bazadan o'qishda har qanday xatolik bo'lsa request.state.user = None bo'lib qoladi
        pass
      finally:
        db.close()

    # 4. Agar so'rov /api bilan boshlansa va user topilmagan bo'lsa 401 qaytarish
    if request.state.user is None and path.startswith("/api"):
      response = JSONResponse(
          status_code=status.HTTP_401_UNAUTHORIZED,
          content={"detail": "Session is expired or invalid token"},
      )
      if token_from_cookie:
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")
      return response

    return await call_next(request)


class TimeCounter(BaseHTTPMiddleware):

  async def dispatch(self, request:Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    time_delta = time.perf_counter()-start_time
    response.headers["X-proccess-time"] = str(time_delta)
    return response