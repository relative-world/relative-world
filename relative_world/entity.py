import logging
import uuid
from typing import Iterator, Annotated, Type, Callable

from pydantic import BaseModel, Field, PrivateAttr

from relative_world.event import Event

logger = logging.getLogger(__name__)

type BoundEvent = tuple[Entity, Event]


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
    _staged_events_for_production: Annotated[list[BoundEvent], PrivateAttr()] = []
    _event_handlers: Annotated[dict[Type[Event], Callable[['Entity', Event], None]], PrivateAttr()] = {}

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

    def set_event_handler(
            self,
            event_type: Type[Event],
            event_handler: Callable[['Entity', Event], None]
    ):
        logger.debug(f"Setting event handler for {event_type}")
        self._event_handlers[event_type] = event_handler

    def clear_event_handler(
            self,
            event_type: Type[Event],
    ):
        logger.debug(f"Clearing event handler for {event_type}")
        self._event_handlers.pop(event_type)

    def handle_event(self, entity, event: Event):
        """
        Handles an event that has been propagated to the entity.

        Args:
            entity (Entity): The entity that the event is propagated to.
            event (Event): The event to handle.
        """
        logger.debug(f"%s received event %s", self.id, event)
        handler = self._event_handlers.get(event.__class__)
        if handler:
            handler(entity, event)
        for child in self.children[::]:
            child.handle_event(entity, event)

    def find_by_id(self, entity_id: uuid.UUID) -> 'Entity':
        """
        Finds an entity by its unique identifier.

        Args:
            entity_id (UUID): The unique identifier of the entity to find.

        Returns:
            Entity: The entity with the specified unique identifier.
        """
        if self.id == entity_id:
            return self
        for child in self.children:
            entity = child.find_by_id(entity_id)
            if entity:
                return entity
        return None

    def update(self) -> Iterator[tuple['Entity', Event]]:
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
            should_propagate = self.propagate_event(event_source, event)
            self.handle_event(event_source, event)
            if should_propagate is True:
                self.emit_event(event, source=event_source)

        yield from self.pop_event_batch_iterator()

    def pop_event_batch_iterator(self) -> Iterator[BoundEvent]:
        """
        Pops the batch of staged events for production.

        Yields:
            Iterator[tuple[Entity, Event]]: An iterator of tuples containing the entity and the event.
        """
        staged_events_for_production, self._staged_events_for_production = (
            self._staged_events_for_production,
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
        self._staged_events_for_production.append((source or self, event))

    def add_entity(self, child: 'Entity'):
        """
        Adds a child entity to the entity.

        Args:
            child (Entity): The child entity to add.
        """
        if child not in self.children:
            self.children.append(child)

    def remove_entity(self, child: 'Entity'):
        """
        Removes a child entity from the entity.

        Args:
            child (Entity): The child entity to remove.
        """
        if child in self.children:
            self.children.remove(child)


