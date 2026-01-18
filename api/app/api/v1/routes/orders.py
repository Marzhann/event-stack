from fastapi import APIRouter, Depends, HTTPException
from kafka import KafkaProducer
from typing import List

from app.api.deps.kafka_deps import get_kafka_producer
from app.auth.dependencies import get_current_user
from app.schemas.order import OrderCreate, OrderRead, OrderBase
from app.api.v1.dependencies.order_deps import get_order_service
from app.schemas.user import UserInDB
from app.services.order_service import OrderService
from app.services.exceptions import OrderNotFoundError


router = APIRouter()

@router.post("", response_model=OrderBase)
def create_order(
        order_in: OrderCreate,
        service: OrderService = Depends(get_order_service),
        producer: KafkaProducer = Depends(get_kafka_producer),
        current_user: UserInDB = Depends(get_current_user),
) -> OrderBase:
    result = service.create(order=order_in, user_id=current_user.id)

    # send an order event to kafka
    service.publish_order_created(producer=producer, order=dict(order_in))

    return result


@router.get("", response_model=List[OrderRead])
def list_orders(service: OrderService = Depends(get_order_service)):
    return service.list()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id:int, service: OrderService = Depends(get_order_service)):
    try:
        return service.get(order_id=order_id)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")

