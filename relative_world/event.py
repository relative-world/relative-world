from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from relative_world.time import utcnow


class Event(BaseModel):
    """
    Event is a base class for all events in the simulation.

    Attributes:
        type (str): The type of the event.
        created_at (datetime): The timestamp when the event was created.
    """

    type: str
    created_at: Annotated[datetime, Field(default_factory=utcnow)]
