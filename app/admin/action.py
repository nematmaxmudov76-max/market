from fastapi import Request, APIRouter
from app.model import User
from app.database import db_dep



# send secred code to "is_active = true" users, and her moving "is_"