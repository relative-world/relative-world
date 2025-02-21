import uuid
from datetime import timedelta, datetime
from typing import Iterator, Annotated

from freezegun import freeze_time
from pydantic import Field

from relative_world.entity import Entity, BoundEvent
from relative_world.location import Location
from relative_world.time import utcnow


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
    simulation_start_time: Annotated[datetime, Field(default_factory=utcnow)]
    time_step: timedelta = timedelta(minutes=15)
    previous_iterations: int = 0
    _locations_by_id: dict[uuid.UUID, Location] = {}

    def __init_subclass__(cls, **kwargs):
        """
        Initializes the subclass with a reentrant lock for thread safety.
        """
        cls._world = synchronize.RLock()
        super().__init_subclass__(**kwargs)

    def update(self) -> Iterator[BoundEvent]:
        """
        Advances the simulation by one time step and updates the state of the world.

        Yields:
            Iterator[BoundEvent]: An iterator of `BoundEvent` instances representing the events that occurred during the update.
        """
        current_time = (
                self.simulation_start_time + self.time_step * self.previous_iterations
        )
        with freeze_time(current_time):
            yield from super().update()
        self.previous_iterations += 1

    def add_location(self, location: Location):
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
        if location:
            actor.location = location

    def remove_location(self, location: Location):
        """
        Adds a location to the world and registers it in the `_locations_by_id` dictionary.

        Args:
            location (Location): The location to be added to the world.
        """
        self._locations_by_id[location.id] = location
        super().add_entity(location)

    def get_location_by_id(self, id: uuid.UUID) -> Location:
        """
        Retrieves a location by its unique identifier.

        Args:
            id (uuid.UUID): The unique identifier of the location.

        Returns:
            Location: The location associated with the given identifier, or None if not found.
        """
        return self._locations_by_id.get(id)
