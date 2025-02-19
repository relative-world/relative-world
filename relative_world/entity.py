import logging
from typing import Self

from pydantic import BaseModel


logger = logging.getLogger(__name__)


class Entity(BaseModel):
    """
    Entity is a base class for all entities in the simulation.

    Attributes:
        children (list[Self]): A list of child entities.
    """

    children: list[Self] = []

    def handle_event(self, event: 'BoundEvent') -> bool:
        """
        Handles an event by applying it to the entity.

        Args:
            event (BoundEvent): The event to handle.

        Return:
            True if the event should propagate further.
        """
        for child in self.children:
            if not child.handle_event(event):
                return False
        return True

    def update(self):
        """
        Updates the state of the entity and its children.

        Applies child events to each child entity as they occur
        """
        for child in self.children:
            for event in child.update():
                if self.handle_event(event):
                    yield event
        yield from []

