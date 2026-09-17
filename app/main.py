from fastapi import FastAPI
from app.config import settings
from app.admin.settings import admin
from .middleware import SessionValidationMiddleware, TimeCounter, limiter
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

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

admin.mount_to(app = app)

app.add_middleware(SessionValidationMiddleware)
app.add_middleware(TimeCounter)

app.add_middleware(
    TrustedHostMiddleware,
    allow_hosts=settings.ALLOWED_HOSTS,
) # yani, bu middleware orqali faqatgina ruxsat berilgan hostlar orqali so'rovlar qabul qilinadi. Bu xavfsizlikni oshiradi.

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) # bu middleware orqali CORS sozlamalari amalga oshiriladi. Bu, boshqa domenlardan keladigan so'rovlarni boshqarish imkonini beradi.

app.state.limiter = limiter

