from typing import Generic, Optional, TypeVar
from datetime import datetime, timezone
from pydantic import BaseModel, Field


T = TypeVar("T", bound=BaseModel)

class EventEnvelope(BaseModel, Generic[T]):
    event_id: str = Field(..., description="UUID string; used for idempotency(inbox)")
    event_type: str = Field(..., description="e.g. 'orders.created'")
    occurred_at: datetime = Field(..., description="UTC timestamp when event happened")
    schema_version: int = Field(1, description="Envelope schema version")
    key: Optional[str] = Field(None, description="Partition key hint (e.g. 'order:234')")
    payload: T

    @classmethod
    def from_payload(
            cls,
            *,
            event_id: str,
            event_type: str,
            payload: T,
            key: Optional[str] = None,
            occurred_at: Optional[datetime] = None,
            schema_version: int = 1,
    ) -> "EventEnvelope[T]":
        """Convenience constructor with sane defaults."""
        return cls(
            event_id=event_id,
            event_type=event_type,
            occurred_at=occurred_at or datetime.now(timezone.utc),
            schema_version=schema_version,
            key=key,
            payload=payload,
        )