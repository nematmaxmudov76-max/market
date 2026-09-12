from datetime import datetime
from pydantic import EmailStr, model_validator
from zxcvbn import zxcvbn
from .base import Base


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


# SESSION AUTH


class UserLoginRequest(Base):
    email: EmailStr
    password: str


class RefreshTokenRequest(Base):
    access_token: str
