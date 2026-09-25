from pydantic import BaseModel, Field


class OneProductDetailsRespones(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=2)
    description: str | None = None
    product_size: float
    price: float = Field(gt=0)
    product_current_count_in_store: int = Field(default=0, ge=0)
    product_rating_avg: float = Field(default=0.0, ge=0.0, le=5.0)
    product_rating_counts: int = Field(default=0, ge=0)
    media_id: int | None = None
    users_comments: int = Field(default=0, ge=0)
    current_price: float = Field(default=0, ge=0)
    discount_title: str = Field(None)
    is_liked: bool = Field(default=False)
