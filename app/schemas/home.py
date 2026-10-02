from .base import Base
from datetime import datetime

class ProductListResponse(Base):
    name: str
    description: str | None = None
    price: float
    discount_id: int | None = None
    current_quantity: int
    expiration_date: datetime | None  = None
    size: float | None = None
    is_active: bool
