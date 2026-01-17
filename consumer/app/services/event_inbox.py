from sqlalchemy.exc import IntegrityError

from consumer.app.core.db import SessionLocal
from consumer.app.models.event_inbox import EventInbox
from datetime import datetime


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
                event_id=str(envelope.event_id),
                event_type=envelope.event_type,
                occurred_at=envelope.occurred_at,
                topic=topic,
                partition=partition,
                offset=offset,
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


    def update_status(self, event_id: str, status: str):
        db = SessionLocal()
        try:
            db.query(EventInbox).filter(
                EventInbox.event_id == event_id,
                EventInbox.status == "RECEIVED",
            ).update(
                {
                    EventInbox.status : status,
                    EventInbox.processed_at: datetime.utcnow() if status == "PROCESSED" else None,
                }
            )

            db.commit()
        finally:
            db.close()


