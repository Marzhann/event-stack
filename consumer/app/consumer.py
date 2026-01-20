from kafka import KafkaConsumer

from datetime import datetime, timezone

from app.core.config import KAFKA_BOOTSTRAP_SERVERS, MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
from app.messaging.events.envelope import from_bytes, EventEnvelope
from app.messaging.events.orders import OrderCreatedPayload
from app.services.event_inbox import EventInboxService
from app.storage.s3 import get_s3_client, put_object, ensure_bucket, MAX_INLINE_BYTES


def main():
    consumer = KafkaConsumer(
        "orders.created",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="debug_consumer",
    )

    print("Consumer started. Waiting for messages...")

    inbox = EventInboxService()
    s3_client = get_s3_client(endpoint_url=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)
    ensure_bucket(s3=s3_client, bucket=MINIO_BUCKET)

    for msg in consumer:
        status = "RECEIVED"
        error: str = None

        try:
            event = from_bytes(EventEnvelope[OrderCreatedPayload], msg.value)
        except Exception as e:
            error = (
                f"[PARSE_ERROR] topic={msg.topic} partition={msg.partition} offset={msg.offset} "
                f"err={type(e).__name__}: {e}"
            )
            event = None
            status = "FAILED_TO_PARSE"
            print(error)

        try:
            raw_json = msg.value.decode("utf-8")
        except UnicodeDecodeError:
            error_msg = (
                f"[DECODE_ERROR] event_id={getattr(event, 'event_id', None)} "
                f"topic={msg.topic} partition={msg.partition} offset={msg.offset}"
            )
            error = error + "\n" + error_msg if error else error_msg
            raw_json = None
            status = "FAILED_TO_DECODE"
            print(error)

        # decide if we push payload to s3
        payload_s3_key = f"{msg.topic}/{msg.partition}/{msg.offset}.bin"
        payload_size_bytes = len(msg.value)

        if raw_json is None:  # decode failed -> always push to s3 bucket
            payload_content_type = "application/octet-stream"
            put_object(
                s3=s3_client,
                key=payload_s3_key,
                bucket=MINIO_BUCKET,
                data=msg.value,
                content_type=payload_content_type
            )
        else:
            if payload_size_bytes > MAX_INLINE_BYTES:  # payload is too big -> push
                raw_json = None
                payload_content_type = "application/json"
                put_object(s3=s3_client,
                    key=payload_s3_key,
                    bucket=MINIO_BUCKET,
                    data=msg.value,
                    content_type=payload_content_type
                )

            else:  # not too big -> store in inbox
                payload_s3_key = None
                payload_content_type = "application/json"


        inserted = inbox.save(
            envelope=event,
            topic=msg.topic,
            partition=msg.partition,
            offset=msg.offset,
            raw_json=raw_json,
            status=status,
            error=error,
            payload_s3_key=payload_s3_key,
            payload_size_bytes=payload_size_bytes,
            payload_content_type=payload_content_type,
        )

        if inserted and not error:
            print(
                f"[INBOX_SAVED] event_id={event.event_id} type={event.event_type} "
                f"topic={msg.topic} p={msg.partition} o={msg.offset}"
            )
            try:
                # processing logic
                pass
                inbox.update_status(
                    event_id=event.event_id,
                    status="PROCESSED",
                )
            except Exception as e:
                inbox.update_status(
                    event_id=event.event_id,
                    status="FAILED_TO_PROCESS",
                    error=str(e)
                )
        else:
            print(
                f"[INBOX_NOT_SAVED/DUPLICATION DETECTED] event_id={getattr(event, 'event_id', None)} (already in inbox) "
                f"topic={msg.topic} p={msg.partition} o={msg.offset}"
            )

        # save kafka offset - confirm delivery
        consumer.commit()




if __name__ == "__main__":
    main()