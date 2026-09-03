

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy import select
from app.database import db_dep
from typing import Annotated
from app.utils import verify_password

from app.model import User

basic = HTTPBasic()
basic_auth = Annotated[HTTPBasicCredentials, Depends(basic)]

def get_current_user(session:db_dep, credention:basic_auth):
    stmt  = select(User).where(User.email == credention.username)

    if not stmt:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(credention.password, User.password_hash):
        raise HTTPException(status_code=401, detail="incorrect password")

    return stmt

current_user_basic = Annotated[User, Depends(get_current_user)]