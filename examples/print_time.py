"""
This script demonstrates a simple simulation where entities in a world can emit and handle events.
The simulation progresses in time steps, and specific actions are performed at each step.

Classes:
    SayAloudEvent: Represents an event where an entity says something aloud.
    TimeLoggerActor: An entity that logs the current time or a tick message at regular intervals.
    MessagePrinter: An entity that prints messages from events it handles.

Usage:
    Run this script to start the simulation. The `TimeLoggerActor` will log the time every fourth iteration,
    and a tick message on other iterations. The `MessagePrinter` entities will print these messages.
"""

import time
from datetime import timedelta

from relative_world.entity import Entity
from relative_world.event import Event, EventType
from relative_world.location import Location
from relative_world.scripted_entity import ScriptKeyPoint, ScriptedEntity
from relative_world.time import utcnow
from relative_world.world import RelativeWorld


class SayAloudEvent(Event):
    """
    Event that represents saying something aloud.

    Attributes:
        type (EventType): The type of the event, set to SAY_ALOUD.
        message (str): The message to be said aloud.
    """
    type: EventType = EventType.SAY_ALOUD
    message: str


class TimeLoggerActor(ScriptedEntity):
    """
    An entity that logs the current time or a tick message at regular intervals.

    Attributes:
        iteration_count (int): The number of iterations the entity has gone through.
    """
    iteration_count: int = 0

    def get_action(self, action: str):
        """
        Returns the method corresponding to the given action name.

        Args:
            action (str): The name of the action.

        Returns:
            Callable: The method corresponding to the action, or None if not found.
        """
        if action == "log_time":
            return self.log_time
        return None

    def log_time(self):
        """
        Logs the current time by emitting a SayAloudEvent with the current time as the message.
        """
        self.emit_event(SayAloudEvent(message=f"The time is {utcnow().isoformat()}", context={}))

    def log_tick(self):
        """
        Logs a tick message by emitting a SayAloudEvent with a tick message.
        """
        self.emit_event(SayAloudEvent(message=f"- Tick -", context={}))

    def update(self):
        """
        Updates the entity's state. Logs the time every fourth iteration, and a tick message on other iterations.

        Yields:
            Iterator[Event]: Events generated by the entity.
        """
        self.iteration_count += 1
        if self.iteration_count % 4 == 0:
            self.log_time()
        else:
            self.log_tick()
        yield from super().update()


class MessagePrinter(Entity):
    """
    An entity that prints messages from events it handles.

    Attributes:
        name (str): The name of the printer.
    """
    name: str

    def handle_event(self, entity, event) -> bool:
        """
        Handles an event by printing the event's message.

        Args:
            entity (Entity): The entity that emitted the event.
            event (Event): The event to handle.

        Returns:
            bool: Always returns True.
        """
        print(f"{self.name} - {event.message}")
        return True


# Create the world
world = RelativeWorld(simulation_start_time=utcnow())

# Create actors
time_logger = TimeLoggerActor(
    script=[
        ScriptKeyPoint(
            timestamp=utcnow() + timedelta(minutes=45),
            action="log_time",
            args=[],
            kwargs={}
        )
    ]
)

oregon_printer = MessagePrinter(name="Oregon")
global_printer = MessagePrinter(name="Global")

# Create locations and add entities to the world
oregon = Location(private=True)
world.add_entity(oregon)
world.add_entity(global_printer)
oregon.add_entity(oregon_printer)
oregon.add_entity(time_logger)

# Run the simulation
while True:
    list(world.update())
    time.sleep(1)