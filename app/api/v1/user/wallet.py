from fastapi import APIRouter, Depends, HTTPException
from app.model.user import Wallet
from app.database import db_dep

router = APIRouter(prefix="/user/wallet", tags=["User Wallet"])

@router.get("/balance")
async def get_currrnet_balace(sesion:db_dep, user_id:int):