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
        id (UUID): The unique identifier for the entity.
        children (list[Entity]): A list of child entities.
        staged_events_for_production (list[Event]): A list of events staged for production.
    """

    id: Annotated[uuid.UUID, Field(default_factory=uuid.uuid4)]
    children: Annotated[list['Entity'], Field(default_factory=list)]
    staged_events_for_production: Annotated[list[Event], Field(default_factory=list)]

    def propagate_event(self, entity, event) -> bool:
        """
        Propagates an event to the entity and its children.

        Args:
            entity (Entity): The entity to propagate the event to.
            event (Event): The event to propagate.

        Returns:
            bool: True if the event should propagate to the parent entity, False otherwise.
        """
        return True

    def handle_event(self, entity, event: Event):
        """
        Handles an event that has been propagated to the entity.

        Args:
            entity (Entity): The entity that the event is propagated to.
            event (Event): The event to handle.
        """
        for child in self.children[::]:
            child.handle_event(entity, event)

    def update(self) -> Iterator[tuple[Self, Event]]:
        """
        Updates the state of the entity and its children.

        Applies child events to each child entity as they occur.

        Yields:
            Iterator[tuple[Entity, Event]]: An iterator of tuples containing the entity and the event.
        """
        event_producers = self.children[::]
        while event_producers:
            producer = event_producers.pop(0)
            try:
                event_source, event = next(producer.update())
            except StopIteration:
                continue
            if self.propagate_event(event_source, event) is False:
                self.handle_event(event_source, event)
            else:
                self.emit_event(event, source=event_source)

        yield from self.pop_event_batch_iterator()

    def pop_event_batch_iterator(self) -> Iterator[tuple[Self, Event]]:
        """
        Pops the batch of staged events for production.

        Yields:
            Iterator[tuple[Entity, Event]]: An iterator of tuples containing the entity and the event.
        """
        staged_events_for_production, self.staged_events_for_production = (
            self.staged_events_for_production,
            [],
        )
        yield from staged_events_for_production[::]

    def emit_event(self, event: Event, source=None):
        """
        Emits an event from the entity.

        Args:
            event (Event): The event to emit.
            source (Entity, optional): The source entity of the event. Defaults to None.
        """
        logger.info(f"%s emitted %s", self.id, event)
        self.staged_events_for_production.append((source or self, event))

    def act(self) -> Iterator[Event]:
        """
        Performs an action and yields any events that result from the action.

        Yields:
            Iterator[Event]: An iterator of events resulting from the action.
        """
        yield from ()

    def add_entity(self, child: Self):
        """
        Adds a child entity to the entity.

        Args:
            child (Entity): The child entity to add.
        """
        if child not in self.children:
            self.children.append(child)

    def remove_entity(self, child: Self):
        """
        Removes a child entity from the entity.

        Args:
            child (Entity): The child entity to remove.
        """
        if child in self.children:
            self.children.remove(child)
