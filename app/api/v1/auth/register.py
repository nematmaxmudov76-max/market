import secrets
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.database import db_dep
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas import UserRegisterRequest, UserRegisterResponse
from app.model import User
from app.utils import hash_password, redis_client
from app.celery import send_email_message

router = APIRouter(prefix="/user-register", tags=["Auth"])


@router.post("", response_model=UserRegisterResponse)
async def create_new_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = (session.execute(stmt)).scalar_one_or_none()

    if res:
        raise HTTPException(status_code=400, detail="user alredy exist")

    user = User(email=data.email, password_hash=hash_password(data.password))

    # send to email kod
    secret_kod = secrets.token_hex(10)
    send_email_message.delay(
        data.email, "Eamil confirmation proccessing", f"your verifay kod{secret_kod}"
    )
    redis_client.setex(secret_kod, 120, user.email) # redis kodni 120 sekund saqlab turadi


    active_user_exists = session.execute(
        select(User.id).where(User.is_deleted.is_(False)).limit(1)
    ).scalar_one_or_none()
    if active_user_exists is None:
        user.is_admin = True
        user.is_staff = True

    session.add(user)
    session.commit()
    session.refresh(user)
    return JSONResponse(
        status_code=201, content={"message":"Send confirmation code to your email, check in gmail!!!"}
    )
@router.post("/verify/{secret_code}", response_model=UserRegisterResponse)
async def verifiy_code(session:db_dep, secret_code:str):
    code = redis_client.get(secret_code)
    print(f" email kod >>>>{code.decode("utf-8")}")

    if not code:
        raise HTTPException(status_code=400, detail="invalid code, your code expired")

    stmt = select(User).where(User.email == code.decode("utf-8"))
    user = (session.execute(stmt)).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    user.is_active = True
    session.commit()
    session.refresh(user)

    return JSONResponse(
        status_code=200, content={"message":"Successful register"}
    )