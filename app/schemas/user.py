from datetime import datetime
from pydantic import EmailStr
from .base import Base


class UserCreateRequest(Base):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
    email: EmailStr
    tell_number: int | None = None
    password_hash: str
    is_active: bool


class UserAddressListResponse(Base):
    user_id: int
    region_id: int
    address: str


class UserListResponse(Base):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    age: int | None = None
    bio: str | None = None
    tell_number: int | None = None
    last_login: datetime
    is_active: bool
    is_staff: bool | None = None
    is_admin: bool | None = None
    is_courier: bool | None = None
    created_at: datetime | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 6,
                    "email": "eshmat@gmail.com",
                    "first_name": "Eshmat",
                    "last_name": "Eshmatov",
                    "bio": "Eshmat yaxshi o'quvchi, lekin u dangasa bilmaydi",
                    "is_active": True,
                    "is_admin": False,
                    "is_staff": False,
                    "created_at": "2026-19-01T13:01:18.001Z",
                }
            ]
        }
    }


class CreateUserLikeRequest(Base):
    user_id: int
    product_id: int
