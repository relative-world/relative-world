import time

from relative_world.actor import Actor
from relative_world.event import Event
from relative_world.time import utcnow
from relative_world.world import RelativeWorld


class StatementEvent(Event):
    type: str = "STATEMENT"
    message: str


class OlYeller(Actor):
    """They yell a lot."""

    def act(self):
        self.emit_event(StatementEvent(message="Hello, world!"))
        yield from super().act()


def echo_handler(source, event):
    print(f"{source.id} says: {event.message}")


if __name__ == "__main__":
    world = RelativeWorld(simulation_start_time=utcnow())

    # create an event producer
    ol_yeller = OlYeller(name="Ol' Yeller")
    world.add_entity(ol_yeller)

    # create an event consumer
    echo_actor = Actor(name="Echo")
    world.add_entity(echo_actor)
    # handle StatementEvent events
    echo_actor.set_event_handler(StatementEvent, echo_handler)
    echo_actor._event_handlers[StatementEvent] = echo_handler

    while True:
        list(world.update())
        time.sleep(1)
