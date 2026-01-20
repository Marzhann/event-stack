from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, Text, DateTime, LargeBinary, UniqueConstraint
from datetime import datetime

from app.core.db import Base

class EventInbox(Base):
    __tablename__ = "event_inbox"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(Text, nullable=True, unique=True)
    event_type: Mapped[str] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    topic: Mapped[str] = mapped_column(Text, nullable=False)
    partition: Mapped[int] = mapped_column(Integer, nullable=False)
    kafka_offset: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # store whole envelope as JSON
    payload_json: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(Text, nullable=False, default="RECEIVED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # failure case
    error: Mapped[str] = mapped_column(Text, nullable=True)
    raw_bytes_64: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    next_retry_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str] = mapped_column(Text, nullable=True)

    # pointer to minio(s3)
    payload_s3_key: Mapped[str] = mapped_column(Text, nullable=True)
    payload_size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    payload_content_type: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("topic", "partition", "kafka_offset", name="uq_event_inbox_msg"),
    )
