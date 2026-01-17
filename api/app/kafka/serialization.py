from pydantic import BaseModel


def to_bytes(event: BaseModel) -> bytes:
    return event.model_dump_json().encode("utf-8")
