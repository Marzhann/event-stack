import uuid
from typing import List, Sequence
from kafka import KafkaProducer
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate, OrderRead, OrderBase
from app.services.exceptions import OrderNotFoundError
from app.models.order import Order
from app.kafka.schemas.orders import OrderCreatedPayload
from app.kafka.schemas.envelope import EventEnvelope
from app.kafka.serialization import to_bytes


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: OrderCreate, user_id: int) -> OrderBase:
        new_order = Order(
            user_id=user_id,
            product_id=order.product_id,
            quantity=order.quantity,
            price_per_unit=order.price_per_unit,
            currency=order.currency,
            total_price=order.quantity * order.price_per_unit,
        )

        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)

        return OrderBase.model_validate(new_order, from_attributes=True)


    def list(self) -> List[OrderRead]:
        orders = self.db.query(Order).all()
        return [
            OrderRead.model_validate(order, from_attributes=True)
            for order in orders
        ]


    def get(self, order_id:int) -> OrderRead:
        order = (
            self.db.query(Order)
            .filter(Order.product_id==order_id)
            .first()
        )

        if not order:
            raise OrderNotFoundError(f"Order {order_id} not found")
        return OrderRead.model_validate(order, from_attributes=True)


    @staticmethod
    def publish_order_created(producer: KafkaProducer, order: dict) -> None:
        payload = OrderCreatedPayload(
            product_id=order["product_id"],
            user_id=order["user_id"],
            quantity=order["quantity"],
            price_per_unit=order["price_per_unit"],
            currency=order["currency"]
        )

        event = EventEnvelope[OrderCreatedPayload].from_payload(
            event_id=str(uuid.uuid4()),
            event_type="orders.created",
            key=f"order={payload.product_id}",
            payload=payload
        )

        producer.send(
            topic="orders.created",
            key=(event.key or "").encode("utf-8"),
            value=to_bytes(event)
        )
        producer.flush(timeout=5)
