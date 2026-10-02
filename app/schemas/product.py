from pydantic import BaseModel, Field
from sqlalchemy import Numeric, DECIMAL

class OneProductDetailsRespones(BaseModel):
    id: int = Field(gt=0) # 0dan kattami m: id != 0
    name: str = Field(min_length=2)
    description: str | None = None
    product_size: Numeric
    category_id:int = Field(ge=0)
    product_current_count_in_store: int = Field(default=0, ge=0)
    product_rating_avg: DECIMAL = Field(default=0.0, ge=0.0, le=5.0)
    product_rating_counts: int = Field(default=0, ge=0)
    media_id: int | None = None
    users_comments: str | None = None
    comment_count:int = Field(default=0)
    price: Numeric = Field(ge=0) # 0 dan katta yoki tengmi?
    discount_title: str = Field(None)
    is_liked: bool = Field(default=False)
