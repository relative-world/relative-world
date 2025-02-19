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


known_actions = {
    "echo": lambda *args, **kwargs: print(args, kwargs),
}

def get_action(action):
    return known_actions[action]


class ScriptedActor(Actor):
    script: list[ScriptKeyPoint]

    def update(self):
        if not self.script:
            return

        next_key_point = self.script[0]
        if next_key_point.timestamp < datetime.now(tz=next_key_point.timestamp.tzinfo):
            action = get_action(next_key_point.action)
            action(*next_key_point.args, **next_key_point.kwargs)
            self.script.pop(0)
