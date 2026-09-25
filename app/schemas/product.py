from pydantic import BaseModel, Field


class OneProductDetails(BaseModel):
    name:str
    description:str | None = None
    price:float = Field(gt=0)
    current_quantity:int | None = None
    size:float
    is_active:bool

