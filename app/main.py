from fastapi import FastAPI


from app.api.v1.user import (
    user_router,
)

app = FastAPI(
    title="Multi-MarketPlase",
    description="Ilovada sotuv, sotib olish, kuryer bo'lish imkoni bor"
)

app.include_router(user_router)