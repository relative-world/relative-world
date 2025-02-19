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
    """
    type: EventType = EventType.SAY_ALOUD
    message: str


class TimeLoggerActor(ScriptedEntity):
    iteration_count: int = 0

    def get_action(self, action: str):
        if action == "log_time":
            return self.log_time
        return None

    def log_time(self):
        self.emit_event(SayAloudEvent(message=f"The time is {utcnow().isoformat()}", context={}))

    def log_tick(self):
        self.emit_event(SayAloudEvent(message=f"- Tick -", context={}))

    def update(self):
        self.iteration_count += 1
        if self.iteration_count % 4 == 0:
            self.log_time()
        else:
            self.log_tick()
        yield from super().update()


class MessagePrinter(Entity):
    name: str

    def handle_event(self, entity, event) -> bool:
        print(f"{self.name} - {event.message}")


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

oregon = Location(private=True)
world.add_entity(oregon)
world.add_entity(global_printer)
oregon.add_entity(oregon_printer)
world.add_entity(time_logger)

while True:
    list(world.update())
    time.sleep(1)
