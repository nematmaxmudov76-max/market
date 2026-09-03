from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator
from zxcvbn import zxcvbn


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password_hash: str
    password2: str

    @model_validator(mode="before")
    def password_validate(self):
        if self.password_hash != self.password2:
            raise ValueError("password xato kititildi")
        if len(self.password_hash) < 8:
            raise ValueError("password 8ta belgidan kam!!")
        if zxcvbn(self.password_hash) and zxcvbn(self.password_hash)["score"] < 4:
            raise ValueError("password zaif")

        return self


class UserRegisterResponse(BaseModel):
    id: int
    email: str
    created_at: datetime
