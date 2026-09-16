
import logging
logger = logging.getLogger("uvicorn.error")
from jose import jwt
from fastapi import Request
from starlette.responses import RedirectResponse, Response
from starlette_admin.auth import AdminUser, AuthProvider
from starlette_admin.exceptions import LoginFailed
from app.config import settings
from app.database import get_db
from app.model import User
from app.utils import generate_jwt_token, verify_password


class JsonAuthProvider(AuthProvider):

  async def login(
      self,
      username: str,
      password: str,
      remember_me: bool,
      request: Request,
  ) -> Response:
    db = next(get_db())
    try:
      user = db.query(User).filter(User.email == username).first()

      if not user or user.is_deleted:
        raise LoginFailed("Foydalanuvchi topilmadi.")

      if not user.is_admin:
        raise LoginFailed("Sizda admin panelga kirish huquqi yo'q.")

      if not verify_password(password, user.password_hash):
        raise LoginFailed("Parol noto'g'ri.")

      # Tokenlarni generatsiya qilish
      access_token, refresh_token = generate_jwt_token(user.id)
      token = refresh_token if remember_me else access_token

      expire_token = (
          settings.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24 # 1 kun
          if remember_me
          else settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 1 soat
      )

      # Muvaffaqiyatli kirgach Admin panel bosh sahifasiga yo'naltirish
      response = RedirectResponse(
          url=request.url_for("admin:index"), status_code=303
      )

      # Cookieni butun domenga biriktirish (path="/")
      response.set_cookie(
          key="access_token",
          value=token,
          httponly=True,
          max_age=expire_token,
          secure=False,  # Lokal muhit (HTTP) uchun False shart
          samesite="lax",
          path="/",  # Juda muhim: cookie butun loyiha bo'yicha ko'rinishi kerak
      )

      return response
    finally:
      db.close()

  async def authenticate(self, request: Request) -> AdminUser | None:
    """Authenticate the admin request using the JWT cookie."""
    # 1. Avval request.state ga qaraydi
    user = getattr(request.state, "user", None)
    logger.warning(f"[auth]1 state.user ->{user}")
    if user and getattr(user, "is_admin", False):
      return AdminUser(username=user.email)

    # 2. Agar state'da user bo'lmasa, cookie'dan 'access_token'ni o'zi oladi
    token = request.cookies.get("access_token")
    logger.warning(f"[auth]2 request.cookie -> {request.cookies}")
    if not token:
      return None

    try:
      # JWT tokenni tekshirish
      payload = jwt.decode(
          token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
      )
      logger.warning(f"[auth]3 decode paylaod ->{payload}")
      user_id = payload.get("sub")
      logger.warning(f"[auth]4 user_id/sub ->{user_id}")
      if not user_id:
        return None

      # Bazadan foydalanuvchini tekshirish
      db = next(get_db())
      try:
        db_user = db.query(User).filter(User.id == int(user_id)).first()
        logger.warning(f"[auth]5 db_user -> {db_user}, is_admin ->{getattr(db_user, "is_admin", None)}, is_deleted ->{getattr(db_user, "is_deleted", None)}")
        if db_user and db_user.is_admin and not db_user.is_deleted:
          # Keyingi requestlar uchun state ga ham yozib qo'yamiz
          request.state.user = db_user
          logger.warning(f"[auth]6 state.user ga saqlandi ->{request.state.user, None}")
          return AdminUser(username=db_user.email)
      finally:
        db.close()

    except Exception as e:
        logger.warning(f"[AUTH DEBUG]7 is_authenticated xatosi: {type(e).__name__}: {e}")
        return None

    logger.warning("[auth] 7oxiriga yetdi false qaytaradi")
    return None

  async def logout(self, request: Request, response: Response) -> Response:
    response.delete_cookie("access_token", path="/")
    return response