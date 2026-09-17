from fastapi import APIRouter, Depends, HTTPException
from app.model.user import Wallet, User
from app.database import db_dep
from sqlalchemy import select
from sqlalchemy import join
router = APIRouter(prefix="/user/wallet", tags=["User Wallet"])

@router.get("/balance/{user_id}")
async def get_currrnet_balace(session:db_dep, user_id:int):
    stmt = (
    select(
        Wallet.balance, 
        Wallet.currency, 
        Wallet.user_id)
    .where(Wallet.user_id == user_id, Wallet.is_blocked == False)
    )
    res = (session.execute(stmt)).scalar_one_or_none()
    if not res:
        raise HTTPException(status_code=404, detail="wallet not found")

    return res
