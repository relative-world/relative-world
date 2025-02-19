import datetime

from pydantic import BaseModel, Field

from relative_world.entity import Entity
from relative_world.event import Event


class BoundEvent(BaseModel):
    """
    An event that is bound to an entity.

    Attributes:
        entity (Entity): The entity that the event is bound to.
    """

    source_entity: Entity
    event: Event
    created_at: datetime.datetime = Field(..., default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))

    def apply(self):
        """
        Applies the event to the entity.
        """
        raise NotImplementedError
