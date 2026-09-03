from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from app.database import db_dep
from app.schemas import UserRegisterResponse
from app.model import User
from app.utils import hash_password

from app.dependense import current_user_basic

router = APIRouter(prefix="/basic_auth", tags=["Authentications"])

@router.post("/profile", response_model=UserRegisterResponse)
async def user_profile(sesion:db_dep, current_user:current_user_basic):
    return current_user


    