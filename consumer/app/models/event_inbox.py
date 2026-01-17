from consumer.app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, BigInteger, Text, DateTime, LargeBinary
from datetime import datetime


class EventInbox(Base):
    __tablename__ = "event_inbox"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id: Mapped[str] = mapped_column(Text, nullable=True, unique=True)
    event_type: Mapped[str] = mapped_column(Text, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    topic: Mapped[str] = mapped_column(Text, nullable=False)
    partition: Mapped[int] = mapped_column(Integer, nullable=False)
    offset: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # store whole envelope as JSON
    payload_json: Mapped[str] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(Text, nullable=False, default="RECEIVED")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    processed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # failure case
    error: Mapped[str] = mapped_column(Text, nullable=True)
    raw_bytes_64: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)


