from fastapi import FastAPI


from app.api.v1 import (
    user_router,
    common_router,
    product_router,
    auth_router,
)

app = FastAPI(
    title="Multi-MarketPlase",
    description="Ilovada sotuv, sotib olish, kuryer bo'lish imkoni bor",
)

app.include_router(user_router)
app.include_router(common_router)
app.include_router(product_router)
app.include_router(auth_router)