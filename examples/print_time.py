import time
from datetime import timedelta

from relative_world.actor import ScriptKeyPoint, ScriptedActor
from relative_world.event import Event, EventType
from relative_world.time import utcnow
from relative_world.world import RelativeWorld


class SayAloudEvent(Event):
    """
    Event that represents saying something aloud.
    """
    type: EventType = EventType.SAY_ALOUD
    message: str


class TimeLoggerActor(ScriptedActor):
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

world.add_entity(time_logger)

print(world.model_dump_json(indent=2))

while True:
    for entity, event in world.update():
        print(world.simulation_start_time, entity.id, event.message)
        time.sleep(1)
