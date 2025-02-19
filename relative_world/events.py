import datetime

from pydantic import BaseModel


class BoundEvent(BaseModel):
    """
    An event that is bound to an entity.

    Attributes:
        entity (Entity): The entity that the event is bound to.
    """

    source_entity: 'Entity'
    created_at: datetime.datetime = datetime.datetime.now(tz=datetime.timezone.utc)

    def apply(self):
        """
        Applies the event to the entity.
        """
        raise NotImplementedError
