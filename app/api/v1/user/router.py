from fastapi import APIRouter

from .wallet import router as wallet_router
from .user import router as user_router
# from .courier import router as courier_router
# dalshe

router = APIRouter(prefix="/api/v1", tags=["User"])

router.include_router(user_router)
router.include_router(wallet_router)
