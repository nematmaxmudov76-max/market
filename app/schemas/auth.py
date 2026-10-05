from datetime import datetime
from pydantic import EmailStr, model_validator
from zxcvbn import zxcvbn
from .base import Base
from app.utils import ManageNotificationCreate, RoleRequestStatus, ChooseRoleRequest


# user register
class UserRegisterRequest(Base):
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def password_validate(self):
        if self.password != self.password2:
            raise ValueError("password xato kititildi")
        if len(self.password) < 8:
            raise ValueError("password 8ta belgidan kam!!")
        if zxcvbn(self.password) and zxcvbn(self.password)["score"] < 2:
            raise ValueError("password zaif")

        return self


class UserRegisterResponse(Base):
    id: int
    email: str
    created_at: datetime


class UserRegisterRoleRequest(Base):
    requested_role: ChooseRoleRequest = None
    application: str

class UserRegisterRoleResponse(Base):
    user_id:int
    requested_role:ChooseRoleRequest
    application:str
    created_at:datetime

# admin action
class AdminMarkedRoleRequest(Base):
    role_request_id: int
    reviewed_at: datetime
    status_expired_at: datetime


class AdminMarkedRoleResponse(Base):
    user_id: int
    request_role: ChooseRoleRequest = None
    checking_status: RoleRequestStatus
    reviewed_by: int
    reviewed_at: datetime
    status_expired_at: datetime


# SESSION AUTH
class UserLoginRequest(Base):
    email: EmailStr
    password: str


class RefreshTokenRequest(Base):
    access_token: str
    refresh_token: str
