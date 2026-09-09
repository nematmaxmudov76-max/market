from fastapi import APIRouter

from .basic import router as basic_auth
from .register import router as register_auth
from .session import router as ssession_auth
from .gwt import router as jwt_auth


router = APIRouter(prefix="/api/v1")

router.include_router(basic_auth)
router.include_router(register_auth)
router.include_router(ssession_auth)
router.include_router(jwt_auth)
