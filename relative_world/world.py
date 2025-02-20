from datetime import timedelta, datetime
from typing import Iterator, Annotated

from freezegun import freeze_time
from pydantic import Field

from relative_world.event import BoundEvent
from relative_world.location import Location
from relative_world.time import utcnow


class RelativeWorld(Location):
    """
    RelativeWorld is an all-encapsulating simulation where time progresses on a defined tick.

    Attributes:
        simulation_start_time (datetime | None): The start time of the simulation.
        time_step (timedelta): The time interval for each simulation tick, defaulting to 15 minutes.
        previous_iterations (int): The number of previous iterations of the simulation.
    """

    simulation_start_time: Annotated[datetime, Field(default_factory=utcnow)]
    time_step: timedelta = timedelta(minutes=15)
    previous_iterations: int = 0

    def update(self) -> Iterator[BoundEvent]:
        """
        Advances the simulation by one time step and updates the state of the world.
        """
        current_time = (
            self.simulation_start_time + self.time_step * self.previous_iterations
        )
        with freeze_time(current_time):
            yield from super().update()
        self.previous_iterations += 1
