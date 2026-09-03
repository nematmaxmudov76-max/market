from fastapi import APIRouter

from .home import router as home_router
from .notification import router as notification_router
from .location import router as location_router


router = APIRouter(prefix="/api/v1")

router.include_router(home_router)
router.include_router(notification_router)
router.include_router(location_router)
