from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.database import db_dep
from app.model import User, User_Notification, Notification
from app.schemas import (
    NotifListResponse,
    NotifCreateResponse,
    NotifUpdateRequest,
)

router = APIRouter(prefix="/notifications", tags=["Notification"])


#  bitda notification_id qayssi userlarga send qilingan
@router.get("/get-users", response_model=NotifListResponse)
async def get_notifications(session: db_dep, notification_id: int):
    stmt = (
        select(User)
        .join(User_Notification, User_Notification.notification_id == notification_id)
        .where(User.is_active == True)
        .order_by(User_Notification.id.desc())
    )
    res = (session.execute(stmt)).scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="user not found")

    return res


# bitda user ga kelgan barcha notificationlar


@router.get("/user-notifications", response_model=NotifListResponse)
async def get_user_notifications(session: db_dep, user_id: int):
    stmt = (
        select(User_Notification)
        .where(User_Notification.user_id == user_id)
        .order_by(User_Notification.id.desc())
    )
    res = (session.execute(stmt)).scalars().all()

    if not res:
        raise HTTPException(status_code=404, detail="notifications not found")

    return res
