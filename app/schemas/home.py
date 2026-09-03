from .base import Base


class ProductListResponse(Base):
    name: str
    description: str
    price: float
    discount_id: int | None = None
    current_quantity: int
    expiration_date: str
    size: float | None = None
    is_active: bool
