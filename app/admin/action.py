from typing import Any
from datetime import datetime, timezone, timedelta
from starlette.requests import Request
from fastapi import APIRouter, HTTPException

from app.model import User, Notification, Role_Request
from app.database import db_dep
from app.schemas import (
    AdminMarkedRoleRequest,
    AdminMarkedRoleResponse,
    )
from app.dependense import current_user_dep, current_admin_dep
from app.config import settings

from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView

from sqlalchemy import select
from sqlalchemy.orm import join


router = APIRouter(prefix="/admin", tags=["Admin"])

"""
get => role_request tabel in users
"""

@router.get("/get/role-aplications")
async def get_role_aplication_users(session:db_dep):
    stmt = (
        select(Role_Request)
        .join(User, User.id == Role_Request.user_id)
        .where(User.is_active == True)
        .order_by(Role_Request.created_at.desc())
    )
    user = (session.execute(stmt)).scalars().all()

    if not user:
        raise HTTPException(status_code=404, detail="users not fount")

    return user


"""
1)checking_status: pending => waiting va exp_time qo'yildi => 
2)userga berilgan exp_time ichida qayta email/sms register qiladi (status = "approved")
3)user login in system => status = "completed"
"""
@router.post("/marked/role", response_model=AdminMarkedRoleResponse)
async def marked_role_user(session:db_dep, data:AdminMarkedRoleRequest, admin_data:current_admin_dep):
    user = session.get(User, Role_Request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    exp_time = datetime.now(timezone.utc)+ timedelta(days=settings.EXP_DATETIME_ROLE_REQUEST * 60 * 60 * 24),
       
    new_user_role = Role_Request(
        user_id = user.id,
        checking_status = data.checking_status,
        reviewed_by = admin_data.id,
        reviewed_at = datetime.now(tz=timezone.utc),
        status_expired_at = exp_time,
    )
    session.add(new_user_role)
    session.commit()

    return new_user_role









