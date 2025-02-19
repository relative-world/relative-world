import logging
from typing import Self, Iterator

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Entity(BaseModel):
    """
    Entity is a base class for all entities in the simulation.

    Attributes:
        children (list[Self]): A list of child entities.
    """

    children: list[Self] = []

    def propagate_event(self, event: 'BoundEvent') -> bool:
        """Propagates an event to the entity and its children.

        Returns True if the event should propagate to the parent entity.
        """
        return all(child.propagate_event(event) for child in self.children[::])

    def update(self) -> Iterator['BoundEvent']:
        """
        Updates the state of the entity and its children.

        Applies child events to each child entity as they occur
        """
        event_producers = self.children[::]
        while event_producers:
            producer = event_producers.pop(0)
            try:
                event = next(producer.update())
            except StopIteration:
                continue
            if self.propagate_event(event):
                yield event

        yield from self.act()

    def act(self) -> Iterator['BoundEvent']:
        """
        Performs an action and yields any events that result from the action.
        """
        yield from ()
