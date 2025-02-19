import enum
from typing import Any

from pydantic import BaseModel


class EventType(str, enum.Enum):
    SAY_ALOUD = "SAY_ALOUD"
    SAY_DIRECTLY = "SAY_DIRECTLY"
    THINK = "THINK"
    MOVE = "MOVE"
    INSPECT = "INSPECT"
    USE = "USE"


class Event(BaseModel):
    type: EventType
    context: dict[str, Any]


