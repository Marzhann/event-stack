from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


Currency = Literal["USD", "EUR", "PLN"]


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = Field(gt=0)
    price_per_unit: float = Field(gt=0)
    currency: Currency = "PLN"


class OrderCreate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    total_price: float
    created_at: datetime

    model_config = {"from_attributes": True}

