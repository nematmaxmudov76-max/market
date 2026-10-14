from fastapi import APIRouter

from .bucked import router as bucked_router

router = APIRouter(prefix="/api/v1")

router.include_router(bucked_router)