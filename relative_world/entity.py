import logging
import uuid
from typing import Self, Iterator, Annotated

from pydantic import BaseModel, Field

from relative_world.event import Event

logger = logging.getLogger(__name__)


class Entity(BaseModel):
    """
    Entity is a base class for all entities in the simulation.

    Attributes:
        children (list[Self]): A list of child entities.
    """
    id: Annotated[uuid.UUID, Field(default_factory=uuid.uuid4)]
    children: Annotated[list[Self], Field(default_factory=list)]
    staged_events_for_production: Annotated[list[Event], Field(default_factory=list)]

    def propagate_event(self, entity, event) -> bool:
        """Propagates an event to the entity and its children.

        Returns True if the event should propagate to the parent entity.
        """
        return all(child.propagate_event(entity, event) is not False for child in self.children[::])

    def update(self) -> Iterator[tuple[Self, Event]]:
        """
        Updates the state of the entity and its children.

        Applies child events to each child entity as they occur
        """
        event_producers = self.children[::]
        while event_producers:
            producer = event_producers.pop(0)
            try:
                event_source, event = next(producer.update())
            except StopIteration:
                continue
            if self.propagate_event(event_source, event) is not False:  # Propagate on None or True
                yield event_source, event

        yield from self.pop_event_batch_iterator()

    def pop_event_batch_iterator(self) -> Iterator[tuple[Self, Event]]:
        staged_events_for_production, self.staged_events_for_production = self.staged_events_for_production, []
        yield from ((self, event) for event in staged_events_for_production[::])

    def emit_event(self, event: Event):
        """
        Emits an event from the entity.
        """
        self.staged_events_for_production.append(event)

    def act(self) -> Iterator[Event]:
        """
        Performs an action and yields any events that result from the action.
        """
        yield from ()

    def add_entity(self, child: Self):
        if child not in self.children:
            self.children.append(child)

    def remove_entity(self, child: Self):
        if child in self.children:
            self.children.remove(child)
