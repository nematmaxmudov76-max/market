from fastapi import APIRouter

from .basic import router as basic_auth


router = APIRouter(prefix="/api/v1")

router.include_router(basic_auth)
