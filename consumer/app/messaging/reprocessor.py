import time
from datetime import datetime, timezone, timedelta

from app.services.event_inbox import EventInboxService


POLL_SECONDS = 5
BACKOFF_INTERVALS = {1: 30, 2: 60, 3: 120}

def main():
    def get_backoff(attempt: int) -> int | None:
        return BACKOFF_INTERVALS.get(attempt, None)

    inbox = EventInboxService()
    print("Reprocessor started. Watching FAILED_TO_PROCESS...")

    while True:
        events = inbox.fetch_failed()

        if not events:
            time.sleep(POLL_SECONDS)
            continue

        for row in events:
            try:
                # processing logic
                inbox.update_status(
                    event_id=row.event_id,
                    status="PROCESSED",
                )
                print(f"[REPROCESSED] event_id={row.event_id}")
            except Exception as e:
                backoff_seconds = get_backoff(row.attempts + 1)
                if backoff_seconds:
                    inbox.update_status(
                        event_id=row.event_id,
                        status="FAILED_TO_PROCESS",
                        error=str(e),
                        attempts_inc=1,
                        next_retry_at=datetime.now(timezone.utc) + timedelta(seconds=backoff_seconds)
                    )
                else:
                    inbox.update_status(
                        event_id=row.event_id,
                        status="DEAD",
                        error=str(e)
                    )

                print(f"[REPROCESS_FAILED] event_id={row.event_id} err={e}")

