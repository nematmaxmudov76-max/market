from fastapi import APIRouter
from .action import router as action_router

router = APIRouter(prefix="/api/v1")

router.include_router(action_router)