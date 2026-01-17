from pydantic import BaseModel


class OrderCreatedPayload(BaseModel):
    product_id: int
    user_id: int
    quantity: int
    price_per_unit: float
    currency: str = "PLN"
