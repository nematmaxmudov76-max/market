from fastapi import FastAPI
from app.config import settings

from app.api.v1 import (
    user_router,
    common_router,
    product_router,
    auth_router,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(common_router)
app.include_router(product_router)
