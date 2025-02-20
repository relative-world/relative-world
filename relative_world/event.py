from typing import Any

from pydantic import BaseModel


class Event(BaseModel):
    type: str
    context: dict[str, Any]


type BoundEvent = tuple['Entity', Event]
