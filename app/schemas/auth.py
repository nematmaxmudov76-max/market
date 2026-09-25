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
    user_id: int
    requested_role: ChooseRoleRequest = None
    application: str
    checking_status: RoleRequestStatus = RoleRequestStatus.PENDING
    status_expires_at: datetime
    hash_code: str | None = None
    reviewed_by: int | None = None
    reviewed_at: datetime | None = None
    attempt_count: int = 0


# SESSION AUTH


class UserLoginRequest(Base):
    email: EmailStr
    password: str


class RefreshTokenRequest(Base):
    access_token: str


"""


class ManageNotificationCreate(Enum):
    SINGLE = "single"
    ALL = "all"
    ACTIVE_USER ="active_users"
    MERCHANTS = "merchants"
    COURIERS = "couriers"
    MANAGERS  = "managers"

class RoleRequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"





    user_id:Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False)
    request_role:Mapped[bool] = mapped_column(Boolean, default="active")
    application:Mapped[Text] = mapped_column(Text, nullable=True)
    resume_url:Mapped[str] = mapped_column(String(250))
    checking_status:Mapped[bool] = mapped_column(Boolean, nullable=True)
    reviewed_by:Mapped[int] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=False)
    reviewed_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    status_expired_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    hash_code:Mapped[str] = mapped_column(String(255), nullable=True)
    attempt_count:Mapped[int] = mapped_column(SmallInteger, default=0)

    
"""
