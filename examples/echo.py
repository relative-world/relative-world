import asyncio

from relative_world.actor import Actor
from relative_world.event import Event
from relative_world.time import utcnow
from relative_world.world import RelativeWorld


# Define a custom event type for statements
class StatementEvent(Event):
    type: str = "STATEMENT"
    message: str


# Define an actor that emits a statement event
class OlYeller(Actor):
    """An actor that yells a message."""

    async def act(self):
        # Emit a StatementEvent with a message
        yield StatementEvent(message="Hello, world!")


# Define a handler function for StatementEvent
async def echo_handler(source, event):
    print(f"{source.id} says: {event.message}")


async def main():
    # Create the world with the current UTC time as the simulation start time
    world = RelativeWorld(simulation_start_time=utcnow())

    # Create an event producer (OlYeller)
    ol_yeller = OlYeller(name="Ol' Yeller")
    world.add_entity(ol_yeller)

    # Create an event consumer (Echo)
    echo_actor = Actor(name="Echo")
    world.add_entity(echo_actor)

    # Set the event handler for StatementEvent
    echo_actor.set_event_handler(StatementEvent, echo_handler)

    # Run the simulation loop
    while True:
        # Update the world, which processes events
        await world.step()
        # Sleep for 1 second before the next update
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
