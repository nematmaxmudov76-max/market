from fastapi import FastAPI
from app.config import settings
from app.admin.settings import admin
from .middleware import SessionValidationMiddleware, TimeCounter, limiter
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
import sqlalchemy.orm.attributes


"""
versiyalar xatoligi sqlalchemy[asyncio] = 2.0.51 versiya starletteni "1.0.1" versiyasiga hali moslashtirilmagan
yechim "Monkey Patching" uslubida yechamiz
"""
# SQLAlchemy ning yangi  versiyalaridagi o'zgarishni starlette_admin uchun moslaymiz
if not hasattr(sqlalchemy.orm.attributes, "ScalarObjectAttributeImpl"):
    sqlalchemy.orm.attributes.ScalarObjectAttributeImpl = getattr(
        sqlalchemy.orm.attributes, "_ScalarObjectAttributeImpl", None
    )

# Qolgan barcha importlaringiz shu yerdan pastda davom etadi:
from app.admin.settings import admin
from fastapi import FastAPI


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

admin.mount_to(app=app)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # chesnok.uz, eshmat.uz *
)  # yani, bu middleware orqali faqatgina ruxsat berilgan hostlar orqali so'rovlar qabul qilinadi. Bu xavfsizlikni oshiradi.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # chesnok.uz, eshmat.uz *
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # bu middleware orqali CORS sozlamalari amalga oshiriladi. Bu, boshqa domenlardan keladigan so'rovlarni boshqarish imkonini beradi.


app.add_middleware(SessionValidationMiddleware)
app.add_middleware(TimeCounter)


app.state.limiter = limiter
