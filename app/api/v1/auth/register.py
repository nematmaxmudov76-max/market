import json
import secrets
from datetime import datetime
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select
from app.database import db_dep
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas import UserRegisterRequest, UserRegisterResponse
from app.model import User
from app.utils import hash_password, redis_client
from app.celery import send_email_message

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
 
    redis_client.setex(secret_kod, 120, json.dumps(user_temp)) # redis kodni 120 sekund saqlab turadi

   # send to email kod
    secret_kod = secrets.token_hex(10)

    send_email_message.delay(
        data.email, 
        "Eamil confirmation proccessing", 
        f"your verifay kod:  {secret_kod}"
    )

    return JSONResponse(
        status_code=201, content={"message":"Send confirmation code to your email, check in gmail!!!"}
    )
@router.post("/verify/{secret_code}", response_model=UserRegisterResponse)
async def verifiy_code(session:db_dep, secret_code:str):
    decode_data = redis_client.get(secret_code)

    if not decode_data:
        raise HTTPException(status_code=400, detail="invalid code, your code expired")
    
    user_data = json.loads(decode_data.decode("utf-8"))
 

    stmt = select(User).where(User.email == user_data["email"])
    user = (session.execute(stmt)).scalar_one_or_none()

    if  user:
        raise HTTPException(status_code=404, detail="user alredy exist")

    new_user = User (
        email = user_data["email"],
        hash_password = user_data["password_hash"],
        is_active = True
    )
    stmt = select(User.id).where(User.is_delete.is_(False)).limit(1)
    existing_user = session.execute(stmt).scalar_one_or_none()

    if existing_user is None:
        new_user.is_admin = True
        new_user.is_staff = True

    session.add(new_user)
    session.commit()
    
    redis_client.delete(secret_code)

    return JSONResponse(
        status_code=200, content={"message":"Successful register"}
    )