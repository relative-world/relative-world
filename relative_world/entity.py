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
    name: str | None = None
    id: Annotated[uuid.UUID, Field(default_factory=uuid.uuid4)]
    children: list['Entity'] = []
    _propagation_queue: Annotated[list[BoundEvent], PrivateAttr()] = []
    _event_handlers: Annotated[dict[Type[Event], Callable[['Entity', Event], None]], PrivateAttr()] = {}

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, id={self.id})"

    def should_propagate_event(self, bound_event: BoundEvent) -> bool:
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
            logger.debug(f"Handling event {event} with handler {handler}")
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
        logger.debug(f"Finding entity by id {entity_id}")
        if self.id == entity_id:
            logger.debug(f"Entity {entity_id} found")
            return self
        for child in self.children:
            entity = child.find_by_id(entity_id)
            if entity:
                logger.debug(f"Entity {entity_id} found in child {child.id}")
                return entity
        logger.debug(f"Entity {entity_id} not found")
        return None

    def update(self) -> Iterator[BoundEvent]:
        """
        Updates the state of the entity and its children.

        Applies child events to each child entity as they occur.

        Yields:
            Iterator[tuple[Entity, Event]]: An iterator of tuples containing the entity and the event.
        """
        logger.debug(f"Updating entity {self.id}")
        event_producers = self.children[::]
        while event_producers:
            producer = event_producers.pop(0)  # grab the next child entity in the list
            logger.debug(f"Processing child entity {producer.id}")

            # see if the child entity has any events to produce
            try:
                event_source, event = next(producer.update())
                logger.debug(f"Child entity {producer.id} produced event {event}")
            except StopIteration:
                logger.debug(f"Child entity {producer.id} has no more events")
                continue

            if self.should_propagate_event((event_source, event)) is not False:
                self.emit_event(event, source=event_source)
            else:
                self.handle_event(event_source, event)


        yield from self.pop_event_batch_iterator()

    def pop_event_batch_iterator(self) -> Iterator[BoundEvent]:
        """
        Pops the batch of staged events for production.

        Yields:
            Iterator[tuple[Entity, Event]]: An iterator of tuples containing the entity and the event.
        """
        logger.debug(f"Popping event batch for entity {self.id}")
        staged_events_for_production, self._propagation_queue = (
            self._propagation_queue,
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
        self._propagation_queue.append((source or self, event))

    def add_entity(self, child: 'Entity'):
        """
        Adds a child entity to the entity.

        Args:
            child (Entity): The child entity to add.
        """
        logger.debug(f"Adding child entity {child.id} to entity {self.id}")
        if child not in self.children:
            self.children.append(child)

    def remove_entity(self, child: 'Entity'):
        """
        Removes a child entity from the entity.

        Args:
            child (Entity): The child entity to remove.
        """
        logger.debug(f"Removing child entity {child.id} from entity {self.id}")
        if child in self.children:
            self.children.remove(child)