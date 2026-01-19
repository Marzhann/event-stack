from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from app.core.db import SessionLocal
from app.models.event_inbox import EventInbox
from datetime import datetime, timezone


class EventInboxService:
    def save(
            self,
            envelope,
            topic: str,
            partition: int,
            offset: int,
            raw_json: str,
            status: str,
            error: str,
            raw_bytes: bytes,
    ) -> bool:
        db = SessionLocal()
        try:
            row = EventInbox(
                event_id=str(getattr(envelope, "event_id", None)),
                event_type=getattr(envelope, "event_type", None),
                occurred_at=getattr(envelope, "occurred_at", None),
                topic=topic,
                partition=partition,
                kafka_offset=offset,
                payload_json=raw_json,
                status=status,
                created_at=datetime.utcnow(),
                error=error,
                raw_bytes_64=raw_bytes,
            )

            db.add(row)
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            return False
        finally:
            db.close()


    def update_status(
            self, event_id: str,
            status: str,
            processed_at: datetime = None,
            # failure case
            error: str = None,
            attempts_inc: int = 0,
            next_retry_at: datetime = None
    ):
        db = SessionLocal()
        try:
            db.query(EventInbox).filter(
                EventInbox.event_id == event_id,
            ).update(
                {
                    EventInbox.status : status,
                    EventInbox.processed_at: datetime.now(timezone.utc) if status == "PROCESSED" else None,
                    EventInbox.error: error,
                    EventInbox.attempts: EventInbox.attempts + attempts_inc,
                    EventInbox.next_retry_at: next_retry_at,
                    EventInbox.last_error: EventInbox.error if error else EventInbox.last_error,
                }
            )

            db.commit()
        finally:
            db.close()

    def fetch_failed(self, limit=50):
        db = SessionLocal()
        try:
            return (
                db.query(EventInbox)
                .filter(
                    EventInbox.status == "FAILED_TO_PROCESS",
                    or_(
                        EventInbox.next_retry_at == None,
                        EventInbox.next_retry_at <= datetime.now(timezone.utc),
                    ),
                )
                .order_by(
                    EventInbox.next_retry_at.asc().nullsfirst(),
                    EventInbox.id.asc(),
                )
                .limit(limit)
                .all()
            )
        finally:
            db.close()

