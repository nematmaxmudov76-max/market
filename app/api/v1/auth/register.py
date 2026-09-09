from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from app.database import db_dep
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.schemas import UserRegisterRequest, UserRegisterResponse
from app.model import User
from app.utils import hash_password


router = APIRouter(prefix="/user-register", tags=["Auth"])


@router.post("/", response_model=UserRegisterResponse)
async def create_new_user(session: db_dep, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = (session.execute(stmt)).scalar_one_or_none()

    if res:
        raise HTTPException(status_code=400, detail="user alredy exist")

    user = User(email=data.email, password_hash=hash_password(data.password))

    stmt2 = session.execute(select(User)).scalars().all()
    if not stmt2:
        user.is_admin = True
        user.is_staff = True

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
