from datetime import datetime
from typing import Any

from relative_world.entity import Entity


class Actor(Entity):

    def tools(self):
        pass

class ScriptKeyPoint(Entity):
    timestamp: datetime
    action: str
    args: list[Any]
    kwargs: dict[str, Any]


class ScriptedActor(Actor):
    script: list[ScriptKeyPoint] = []

    def get_action(action):
        raise NotImplementedError

    def update(self):
        while self.script and self.script[0].timestamp < datetime.now(tz=self.script[0].timestamp.tzinfo):
            next_key_point = self.script.pop(0)
            action = self.get_action(next_key_point.action)
            action(*next_key_point.args, **next_key_point.kwargs)
