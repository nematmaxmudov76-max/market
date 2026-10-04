from typing import Any
from datetime import datetime, timezone, timedelta
from starlette.requests import Request
from fastapi import APIRouter, HTTPException, Depends
from app.celery import send_email_message

from app.model import User, Notification, Role_Request
from app.database import db_dep
from app.schemas import (
    AdminMarkedRoleRequest,
    AdminMarkedRoleResponse,
    )
from app.dependense import  current_admin_dep, current_active_user_dep
from app.config import settings

from starlette_admin import action
from starlette_admin.contrib.sqla import ModelView

from sqlalchemy import select
from sqlalchemy.orm import join

from app.utils import RoleRequestStatus

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
2)user_id
"""

@router.post("/marked/role", response_model=AdminMarkedRoleResponse)
async def marked_role_user(session:db_dep, data:AdminMarkedRoleRequest, admin_data:current_admin_dep, user:current_active_user_dep):
    role_request = session.get(Role_Request, data.role_request_id)
    if not role_request:
        raise HTTPException(status_code=404, detail="Role request not found")




    

    # add data to Role_Request table
    exp_time = datetime.now(timezone.utc)+ timedelta(days=settings.EXP_DATETIME_ROLE_REQUEST)

    role_request.checking_status = RoleRequestStatus.WAITING
    role_request.reviewed_by = admin_data.id
    role_request.reviewed_at = datetime.now(tz=timezone.utc)
    role_request.status_expired_at = exp_time

    session.add(role_request)
    session.commit()
    session.refresh(role_request)

    return role_request









