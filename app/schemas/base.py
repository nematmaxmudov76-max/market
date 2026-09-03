from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Base(BaseModel):
    """
    Mana shu sozlama ORM obyektini(user.post, user.email)
    Json formatga o'girib beradi(user["post"], user["email"])
    """

    model_config = ConfigDict(from_attributes=True)
