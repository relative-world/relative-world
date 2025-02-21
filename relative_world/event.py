from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from relative_world.time import utcnow


class Event(BaseModel):
    type: str
    created_at: Annotated[datetime, Field(default_factory=utcnow)]
