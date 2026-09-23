import json
import shutil
import secrets
from datetime import datetime
from fastapi import HTTPException, APIRouter, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.database import db_dep
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas import (
    UserRegisterRequest,
    UserRegisterResponse,
    UserRegisterRoleRequest,
)
from app.model import User, Role_Request
from app.utils import (
    hash_password,
    redis_url,
    ManageNotificationCreate,
    RoleRequestStatus,
)
from app.celery import send_email_message
from app.config import settings
from pathlib import Path


router = APIRouter(prefix="/user", tags=["Auth"])


@router.post("/register", response_model=UserRegisterResponse)
async def create_new_user(session: db_dep, data: UserRegisterRequest):
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


@router.post("/verify/{secret_code}", response_model=UserRegisterResponse)
async def verifiy_code(session: db_dep, secret_code: str):
    decode_data = redis_url.get(secret_code)

    if not decode_data:
        raise HTTPException(status_code=400, detail="invalid code, your code expired")

    user_data = json.loads(decode_data.decode("utf-8"))

    print(f"decoded data:>>>>>>>> {user_data}")

    stmt = select(User).where(User.email == user_data["email"])
    user = (session.execute(stmt)).scalar_one_or_none()

    if user:
        raise HTTPException(status_code=404, detail="user alredy exist")

    new_user = User(
        email=user_data["email"],
        password_hash=user_data["password_hash"],
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

    return JSONResponse(status_code=200, content={"message": "Successful register"})


# middleware da default => is_active = true larhgina ariza topshira olishi va emailni tasdiqlashi kerak
@router.post("/register/role", response_model=UserRegisterResponse)
async def create_new_user_role(
    session: db_dep, data: UserRegisterRoleRequest, file: UploadFile = None
):
    stmt = select(User).where(User.id == data.user_id, User.is_deleted.is_(False))
    res = (session.execute(stmt)).scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    stmt = select(Role_Request).where(
        Role_Request.user_id == data.user_id,
        Role_Request.request_role == data.requested_role,
    )
    res = (session.execute(stmt)).scalar_one_or_none()
    if res:
        raise HTTPException(
            status_code=403, 
            detail="user already registered before"
            )

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
        media_path = file_path/file.filename
        with open(media_path, "wb") as pth:
            shutil.copyfileobj(file.file, pth)

        db_file = Role_Request(
            resume_url = f"{settings.MEDIA_PATH}/{file.filename}"
        )
        session.add(db_file)
        session.flush()

    new_application = Role_Request(
        user_id = data.user_id,
        request_role = data.requested_role,
        application = data.application,
        checking_status = data.checking_status,
        checking_status = RoleRequestStatus.PENDING
    )
    session.add(new_application)
    session.commit()

    return JSONResponse(
        status_code=201,
        content={"message": "Role request submitted successfully."},
    )





"""

async def create_upload_file(file: UploadFile, db: db_dep):
    if file.size > settings.FILE_SIZE:
        raise HTTPException(
            status_code=400, detail="File size is too large. Max size is 5MB."
        )

    file_ext = Path(file.filename).suffix.lower()  # image.png
    if file_ext not in settings.FILE_TYPE:
        raise HTTPException(
            status_code=400,
            detail="File type is not supported. Only .jpg, .png, .jpeg, .pdf, .docx, .doc, .txt are allowed.",
        )
    path = Path(settings.MEDIA_PATH)
    path.mkdir(exist_ok=True)
    res = path / file.filename  # chesnokuz/media/filename.jpg
    with open(res, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image = Media(url=f"{settings.MEDIA_PATH}/{file.filename}")
    db.add(image)
    db.commit()
    db.refresh(image)

    return {"media_id": image.id, "url": f"{settings.BASE_URL}/{image.url}"}

"""
