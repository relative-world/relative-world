from datetime import timedelta, datetime

from freezegun import freeze_time

from relative_world.entity import Entity


class RelativeWorld(Entity):
    """
    RelativeWorld is an all-encapsulating simulation where time progresses on a defined tick.

    Attributes:
        simulation_start_time (datetime | None): The start time of the simulation.
        time_step (timedelta): The time interval for each simulation tick, defaulting to 15 minutes.
        previous_iterations (int): The number of previous iterations of the simulation.
    """

    simulation_start_time: datetime | None = None
    time_step: timedelta = timedelta(minutes=15)
    previous_iterations: int = 0

    def update(self):
        """
        Advances the simulation by one time step and updates the state of the world.
        """
        current_time = (
            self.simulation_start_time + self.time_step * self.previous_iterations
        )
        with freeze_time(current_time):
            super().update()
