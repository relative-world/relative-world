import uuid
from datetime import timedelta, datetime
from typing import AsyncIterator, Annotated

from pydantic import PrivateAttr

from relative_world.entity import BoundEvent
from relative_world.location import Location


class RelativeWorld(Location):
    """
    Represents an all-encapsulating simulation where time progresses on a defined tick.

    The `RelativeWorld` class is responsible for managing the simulation environment, including the progression of time,
    the addition and removal of entities, and the retrieval of locations by their unique identifiers.

    Attributes:
        simulation_start_time (datetime | None): The start time of the simulation. Defaults to the current UTC time.
        time_step (timedelta): The time interval for each simulation tick, defaulting to 15 minutes.
        previous_iterations (int): The number of previous iterations of the simulation.
        _locations_by_id (dict[uuid.UUID, Location]): A dictionary mapping location IDs to `Location` instances.
    """
    previous_iterations: int = 0
    _locations: Annotated[dict[uuid.UUID, Location], PrivateAttr()] = {}
    _connections: Annotated[dict[uuid.UUID, set[uuid.UUID]], PrivateAttr()] = {}

    async def update(self) -> AsyncIterator[BoundEvent]:
        """
        Advances the simulation by one time step and updates the state of the world.

        Yields:
            AsyncIterator[BoundEvent]: An iterator of `BoundEvent` instances representing the events that occurred during the update.
        """
        async for event in super().update():
            yield event
        self.previous_iterations += 1

    def add_location(self, location: Location):
        """
        Adds a location to the world and registers it in the `_locations_by_id` dictionary.

        Args:
            location (Location): The location to be added to the world.
        """
        self._locations[location.id] = location
        if location.id not in self._connections:
            self._connections[location.id] = set()
        self.add_entity(location)

    def get_location(self, location_id: uuid.UUID) -> Location:
        """Get a location by its ID."""
        return self._locations[location_id]

    def connect_locations(self, location_a: uuid.UUID, location_b: uuid.UUID) -> None:
        """Create a bidirectional connection between two locations."""
        if location_a not in self._locations or location_b not in self._locations:
            raise ValueError("Both locations must exist in the world")

        self._connections[location_a].add(location_b)
        self._connections[location_b].add(location_a)

    def get_connected_locations(self, location_id: uuid.UUID) -> list[Location]:
        """Get all locations connected to the given location."""
        if location_id not in self._connections:
            return []
        return [self._locations[loc_id] for loc_id in self._connections[location_id]]

    def iter_locations(self) -> AsyncIterator[Location]:
        """
        Iterate over all locations in the world.

        Yields:
            AsyncIterator[Location]: An iterator of `Location` instances in the world.
        """
        for location in self.children:
            if isinstance(location, Location):
                yield location

    def remove_location(self, location: Location):
        """
        Adds a location to the world and registers it in the `_locations_by_id` dictionary.

        Args:
            location (Location): The location to be added to the world.
        """
        self._locations_by_id[location.id] = location
        super().add_entity(location)

    def add_actor(self, actor, location=None):
        """
        Add an actor to the location.

        Parameters
        ----------
        actor : Actor
            The actor to be added to the location.
        """
        actor.world = self
        actor.location = location or self
        actor.location.add_entity(actor)

    async def step(self):
        async for _ in self.update():
            pass
