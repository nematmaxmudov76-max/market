from .user import user_router
from .common import common_router
from .product import product_router
from .auth import auth_router

all = [
    "user_router",
    "common_router",
    "product_router",
    "auth_router",
]
