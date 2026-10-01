from fastapi import APIRouter
from .action import router 

action_router = APIRouter(prefix="/api/v1")

router.include_router(action_router)