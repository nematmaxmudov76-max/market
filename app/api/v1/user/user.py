from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.model import User  
from app.schemas.user import UserListResponse,  UserCreateRequest
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create/")
async def create_user(data:UserCreateRequest, session:Session = Depends(get_db)):
    users = User(
        id = data.id,
        first_name = data.first_name,
        last_name = data.last_name,
        age = data.age,
        email = data.email,
        tell_number = data.tell_number,
        password = data.password,
        password_hash = data.password_hash,
        is_active = data.is_active, 
    )
    session.add(users)
    session.commit()
    session.refresh(users)

    return users

# query paramda list ko'rinishida bizga malumot yetib keladi
# TODO get active is true user
@router.get("/", response_model=list[UserListResponse])
async def get_users(is_active:bool | None, session:Session = Depends(get_db)):
    users = select(User)

    if is_active is False:
        raise HTTPException(detail="user don't created yet")
    stmt = users.order_by(User.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()



    