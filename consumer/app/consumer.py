from kafka import KafkaConsumer

from consumer.app.core.config import KAFKA_BOOTSTRAP_SERVERS
from consumer.app.messaging.events.envelope import from_bytes, EventEnvelope
from consumer.app.messaging.events.orders import OrderCreatedPayload
from consumer.app.services.event_inbox import EventInboxService


def main():
    consumer = KafkaConsumer(
        "orders.created",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="debug_consumer",
    )

    print("Consumer started. Waiting for messages...")

    inbox = EventInboxService()

    for msg in consumer:
        status = "RECEIVED"
        error = None

        try:
            event = from_bytes(EventEnvelope[OrderCreatedPayload], msg.value)
        except Exception as e:
            error = (
                f"[PARSE_ERROR] topic={msg.topic} partition={msg.partition} offset={msg.offset} "
                f"err={type(e).__name__}: {e}"
            )
            event = None
            status = "FAILED"
            print(error)

        try:
            raw_json = msg.value.decode("utf-8")
        except UnicodeDecodeError:
            error = (
                f"[DECODE_ERROR] event_id={getattr(event, 'event_id', None)} "
                f"topic={msg.topic} partition={msg.partition} offset={msg.offset}"
            )
            raw_json = None
            status = "FAILED"
            print(error)

        inserted = inbox.save(
            envelope=event,
            topic=msg.topic,
            partition=msg.partition,
            offset=msg.offset,
            raw_json=raw_json,
            status=status,
            error=error,
            raw_bytes=msg.value if not raw_json else None,
        )

        if inserted and status != "FAILED":
            print(
                f"[INBOX_SAVED] event_id={event.event_id} type={event.event_type} "
                f"topic={msg.topic} p={msg.partition} o={msg.offset}"
            )

            try:
                # processing logic
                pass
                inbox.update_status(event_id=event.event_id, status="PROCESSED")
            except Exception as e:
                inbox.update_status(event_id=event.event_id, status="FAILED_TO_PROCESS")
        else:
            print(
                f"[INBOX_NOT_SAVED] event_id={event.event_id} (already in inbox) "
                f"topic={msg.topic} p={msg.partition} o={msg.offset}"
            )





if __name__ == "__main__":
    main()