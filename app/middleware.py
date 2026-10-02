import time
from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import get_db  # get_db o'rniga SessionLocal
from app.model import User
from app.utils import decode_jwt_token
from app.config import (
    INCLUDE_PATHS_ONLY_LOGIN,
    INCLUDE_PATH_ACTIVE_USER,
    INCLUDE_PREFIXES_USERS,
    INCLUDE_PATH_ACTIVE_USER,
)
from jose import JWTError
from slowapi import Limiter
from slowapi.util import get_remote_address


# THIS MIDDLEWARE SCAN ONLY => MANAGER/COURIYER/MERCHANT/ADMIN
class SessionValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request.state.user = None
        path = request.url.path

     
        # 2. Authorization Header yoki Cookie'dan tokenni olish
        auth_header = request.headers.get("Authorization")
        token = None
        token_from_cookie = False

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        else:
            token = request.cookies.get("access_token") or request.cookies.get(
                "refresh_token"
            )
            if token:
                token_from_cookie = True

        # 3. Tokenni dekod qilish va foydalanuvchini bazadan qidirish
        if token:
            try:
                token_payload = decode_jwt_token(token)
                if token_payload:
                    user_id = token_payload.get("sub")
                    exp_time = token_payload.get("exp")

                    # Unix timestamp orqali vaqtni tekshirish
                    current_timestamp = int(time.time())
                    if user_id and exp_time and int(exp_time) > current_timestamp:
                        request.state.user = token_payload# faqat login qilgan userlar fazasi!!!

            except Exception:
                # JWT dekod qilishda yoki bazadan o'qishda har qanday xatolik bo'lsa request.state.user = None bo'lib qoladi
                request.state.user = None


        is_public_path = (path in INCLUDE_PATH_ACTIVE_USER) or (path in INCLUDE_PREFIXES_USERS)

        if not is_public_path and request.state.user is None:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Session is expired or invalid token, please login to system"},
            )
            if token_from_cookie:
                response.delete_cookie("access_token", path="/")
                response.delete_cookie("refresh_token", path="/")
            return response

        if request.state.user:
            active_user = request.state.user.get("is_active", True)
            if not active_user and not is_public_path:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"message":"your account not active, please register to system"}
                )

        response = await call_next(request)

        proccess_time=time.perf_counter() - start_time
        response.headers["X-Middleware-time"] = f"{proccess_time}"

        return response


class TimeCounter(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        time_delta = time.perf_counter() - start_time
        response.headers["X-proccess-time"] = str(time_delta)
        return response


limiter = Limiter(key_func=get_remote_address)


"""
when is_active = false
=> look at home page only (by select product)

active  | => ActiveUserPermission 



"""


# class ActiveUserPermissions(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         path = request.url.path

#         if request.state.user is None :
#             if path in INCLUDE_PATH_ACTIVE_USER or path.startswith(tuple(
#                 INCLUDE_PREFIXES_USERS
#             )):
#                 return await call_next(request)

#         # agar register qilingan bo'lsa request.state.user dan teshkirib oladi
#         user:User | None = getattr(request.state, "user", None)

#         if not user or getattr(user, "is_active", False):
#             return JSONResponse(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 content={"message":"Your not permissions, please register in system"}
#             )


#         if path in INCLUDE_PATH_ACTIVE_USER and path.startswith(tuple(INCLUDE_PATH_ACTIVE_USER)):
#             return await call_next(request)
    
#         auth_header = request.headers.get("Authorization")

#         if not auth_header or not auth_header.startswith("Bearer "):
#             return JSONResponse(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 content={
#                     "message": "You don't have permission, please going to login!!"
#                 },
#             )

#         response = await call_next(request)
#         return response


# class AdminOnlyPermissions(BaseHTTPMiddleware):
#     async def dispatch(self, request:Request, call_next):
#         request.state.user = None
#         path = request.url.path

#         if path not in INCLUDE_ADMIN_PATH:
#             return call_next(request)

        
#         auth_header = request.headers.get("Authorization")

        