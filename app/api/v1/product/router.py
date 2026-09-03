from fastapi import APIRouter
from .product import router as product_router


router = APIRouter(prefix="/api/v1", tags=["Product"])

router.include_router(product_router)
