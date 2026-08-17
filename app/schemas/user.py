from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreateRequest(BaseModel):
    id:int
    first_name:str | None = None
    last_name:str | None = None
    age:int | None = None
    email:EmailStr
    tell_number:int | None = None
    password:str
    password_hash:str
    is_active:bool 

class UserAddressListResponse(BaseModel):
    user_id:int
    region_id:int
    address:str

class UserListResponse(BaseModel):
    firs_name:str | None = None
    last_name:str | None = None
    email:EmailStr
    age:int | None = None
    bio:str | None = None 
    tell_number:int | None = None
    last_login: datetime 
    is_active:bool | None = None
    is_staff:bool  | None = None  
    is_admin:bool | None = None
    created_at:datetime
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 6,
                    "email": "eshmat@gmail.com",
                    "password_hash": "eshmat123",
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

# Mana shu sozlama ORM obyektini(user.post, user.email) Json formatga o'girib beradi(user["post"], user["email"])
    model_config = ConfigDict(from_attributes=True)
