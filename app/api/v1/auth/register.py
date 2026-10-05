import json
import shutil
import secrets
import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, APIRouter, UploadFile, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.database import db_dep
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserRegisterRoleRequest,
    UserRegisterRoleResponse,
)
from app.model import User, Role_Request
from app.utils import (
    hash_password,
    generate_jwt_token,
    verify_password,
    decode_jwt_token,
    redis_url,
    ManageNotificationCreate,
    RoleRequestStatus,
)
from app.celery import send_email_message
from app.config import settings
from pathlib import Path
from app.dependense import current_active_user_dep
from starlette.responses import RedirectResponse, Response



router = APIRouter(prefix="/user/auth", tags=["Auth"])


# active user => get access_token
@router.post("/register", response_model=UserRegisterResponse)
async def create_new_user(session: db_dep, data: UserRegisterRequest, request: Request):
    stmt = select(User).where(User.email == data.email)
    res = (session.execute(stmt)).scalar_one_or_none()

    if res and res.is_active:
        raise HTTPException(status_code=400, detail="user alredy exist")

    user_temp = {
        "email": data.email,
        "password_hash": hash_password(data.password),
        "is_active": False,
    }

    secret_kod = secrets.token_hex(10)
    redis_url.setex(
        secret_kod, 120, json.dumps(user_temp)
    )  # redis kodni 120 sekund saqlab turadi

    # send to email kod

    send_email_message.delay(
        data.email, "Eamil confirmation proccessing", f"your verifay kod:  {secret_kod}"
    )

    return JSONResponse(
        status_code=201,
        content={"message": "Send confirmation code to your email, check in gmail!!!"},
    )


# get access tokent
@router.post("/verify/{secret_code}", response_model=UserRegisterResponse)
async def verifiy_code(session: db_dep, secret_code: str, request: Request):
    decode_data = redis_url.get(secret_code)

    if not decode_data:
        raise HTTPException(status_code=400, detail="invalid code, your code expired")

    user_data = json.loads(decode_data.decode("utf-8"))

    print(f"decoded data:>>>>>>>> {user_data}")

    stmt = select(User).where(
        User.email == user_data["email"], User.is_deleted == False
    )
    user = (session.execute(stmt)).scalar_one_or_none()

    if user:
        raise HTTPException(status_code=404, detail="user alredy exist")

    access_token, refresh_token = generate_jwt_token(user.id)

    # Muvaffaqiyatli kirgach Admin panel bosh sahifasiga yo'naltirish
    response = RedirectResponse(url=request.url_for("admin:index"), status_code=201)

    # Cookieni butun domenga biriktirish (path="/")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 1 hours
        secure=settings.SECURE_DISPATCH,  # Lokal muhit (HTTP) uchun False shart
        samesite="lax",
        path="/",  # Juda muhim: cookie butun loyiha bo'yicha ko'rinishi kerak
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 60 * 60 * 24,  # 1 days
        secure=settings.SECURE_DISPATCH,  # Lokal muhit (HTTP) uchun False shart
        samesite="lax",
        path="/",  # Juda muhim: cookie butun loyiha bo'yicha ko'rinishi kerak
    )

    new_user = User(
        email=user_data["email"],
        password_hash=user_data["password_hash"],
        created_at=datetime.now(tz=timezone.utc),
        is_active=True,
        is_deleted=False,
    )

    stmt = select(User.id).where(User.is_deleted.is_(False)).limit(1)
    existing_user = session.execute(stmt).scalar_one_or_none()

    if existing_user is None:
        new_user.is_admin = True
        new_user.is_staff = True

    session.add(new_user)
    session.commit()

    redis_url.delete(secret_code)

    return new_user


# middleware da default => is_active = true larhgina ariza topshira olishi va emailni tasdiqlashi kerak
@router.post("/register/role", response_model=UserRegisterRoleResponse)
async def create_new_user_role(
    session: db_dep,
    data: UserRegisterRoleRequest,
    file: UploadFile | None,
    current_user: current_active_user_dep,
):
    stmt = select(User).where(User.id == current_user.id, User.is_deleted.is_(False))
    res = (session.execute(stmt)).scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    stmt = select(Role_Request).where(
        Role_Request.user_id == data.user_id,
        Role_Request.request_role == data.requested_role,
    )
    res = (session.execute(stmt)).scalar_one_or_none()
    if res:
        raise HTTPException(status_code=403, detail="user already registered before")

    if file is not None:
        if file.size > settings.FILE_SIZE:
            raise HTTPException(status_code=400, detail="file size too large,")
        file_type = Path(file.filename).suffix.lower()
        if file_type not in settings.FILE_TYPE:
            raise HTTPException(
                status_code=400,
                detail="file not support, only .pdf, .jpg .png .doc .txt .jpeg",
            )
        file_path = Path(settings.MEDIA_PATH)
        file_path.mkdir(exist_ok=True)
        media_path = file_path / file.filename
        with open(media_path, "wb") as pth:
            shutil.copyfileobj(file.file, pth)

        db_file = Role_Request(resume_url=f"{settings.MEDIA_PATH}/{file.filename}")

    new_application = Role_Request(
        user_id=data.user_id,
        request_role=data.requested_role,
        application=data.application,
        resume_url=db_file,
        checking_status=RoleRequestStatus.PENDING,
        created_at=datetime.now(tz=timezone.utc),
    )
    session.add(new_application)
    session.commit()

    return new_application


@router.post("/refresh_tokens")
async def refresh_auth_token(session: db_dep, request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="refresh token not found or token expired",
        )

    decode_refresh = decode_jwt_token(refresh_token)
    if decode_refresh is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail="your refresh token expired"
        )

    user_id = int(decode_refresh["sub"])
    user_obj = session.get(User, user_id)
    if not user_obj or user_obj.is_deleted or not user_obj.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="user not active")

    access_token = generate_jwt_token(user_id, only_access=True)

    response = JSONResponse({"message": "Created new access token"})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=settings.SECURE_DISPATCH,
    )
    return response
