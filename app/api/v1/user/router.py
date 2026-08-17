from    fastapi import APIRouter

from .user import router as user_router
# from .courier import router as courier_router
#dalshe

router = APIRouter(prefix="/api/v1/user", tags=["User"])

router.include_router(user_router)