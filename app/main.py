import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.config import settings
from app.database import Base, DB_URL, engine
import app.model  # noqa: F401 - SQLAlchemy jadvallarini ro'yxatdan o'tkazish
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

# SQLite (vaqtinchalik Vercel demo) rejimida jadvallarni avtomatik yaratish
if DB_URL.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

# Qolgan barcha importlaringiz shu yerdan pastda davom etadi:
from app.admin.settings import admin

from app.admin import admin_router
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


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/static/home-page.html")


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)
app.include_router(common_router)
app.include_router(product_router)

from starlette.staticfiles import StaticFiles
admin.mount_to(app=app)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static", html=True), name="static")

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
