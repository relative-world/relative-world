import asyncio
import uuid
from typing import Annotated, AsyncIterator

from pydantic import PrivateAttr, computed_field

from relative_world.entity import Entity, BoundEvent
from relative_world.event import Event
from relative_world.location import Location
from relative_world.world import RelativeWorld


class Actor(Entity):
    """
    Represents an actor within a relative world.

    Attributes
    ----------
    _world : RelativeWorld | None
        The world in which the actor exists.
    location_id : uuid.UUID
        The unique identifier for the actor's location.

    Parameters
    ----------
    world : RelativeWorld | None, optional
        The world in which the actor exists.
    data : dict, optional
        Additional data for the actor.
    """

    _world: Annotated[RelativeWorld | None, PrivateAttr()] = None
    location_id: uuid.UUID | None = None

    def __init__(self, *, world=None, **data):
        """
        Initializes a new actor.

        Parameters
        ----------
        world : RelativeWorld | None, optional
            The world in which the actor exists.
        data : dict, optional
            Additional data for the actor.
        """
        super().__init__(**data)
        self._world = world

    @computed_field
    @property
    def world(self) -> RelativeWorld | None:
        """
        Gets the world in which the actor exists.

        Returns
        -------
        RelativeWorld | None
            The world in which the actor exists.
        """
        return self._world

    @world.setter
    def world(self, value):
        """
        Sets the world in which the actor exists.

        Parameters
        ----------
        value : RelativeWorld
            The new world for the actor.
        """
        self._world = value
        self.location = value

    @computed_field
    @property
    def location(self) -> Location | None:
        """
        Gets the location of the actor within the world.

        Returns
        -------
        Location | None
            The location of the actor.
        """
        if not self.location_id:
            return None
        if world := self.world:
            return world.get_location(self.location_id)
        return None

    @location.setter
    def location(self, value):
        """
        Sets the location of the actor within the world.

        Parameters
        ----------
        value : Location
            The new location for the actor.
        """
        if self.location:
            self.location.remove_entity(self)
        self.location_id = value.id

    async def update(self) -> AsyncIterator[BoundEvent]:
        """
        Updates the actor's state and propagates events.

        This method filters and yields events that should be propagated based on the actor's
        `should_propagate_event` method. It also calls the superclass's `update` method to
        ensure any additional updates are performed.

        Yields
        ------
        AsyncIterator[BoundEvent]
            An iterator of `BoundEvent` instances representing the events that should be propagated.
        """
        async for event in aiter(self.act()):
            if self.should_propagate_event(event):
                yield self, event
        async for bound_event in super().update():
            yield bound_event

    async def act(self):
        """
        Defines the actions performed by the actor.

        This method should be overridden by subclasses to define the specific actions
        that the actor performs. By default, it yields no events.

        Yields
        ------
        AsyncIterator[Event]
            An iterator of `Event` instances representing the actions performed by the actor.
        """
        for _ in range(0):
            yield