from datetime import datetime
from typing import Any

from relative_world.entity import Entity


class Actor(Entity):
    """
    Actor is a subclass of Entity that represents an actor in the simulation.
    """

    def get_action(self, action: str):
        """
        Retrieves the action method corresponding to the given action name.

        Args:
            action (str): The name of the action to retrieve.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError


class ScriptKeyPoint(Entity):
    """
    ScriptKeyPoint represents a key point in a script for a ScriptedActor.

    Attributes:
        timestamp (datetime): The time at which the action should be performed.
        action (str): The action to be performed.
        args (list[Any]): The positional arguments for the action.
        kwargs (dict[str, Any]): The keyword arguments for the action.
    """
    timestamp: datetime
    action: str
    args: list[Any]
    kwargs: dict[str, Any]


class ScriptedActor(Actor):
    """
    ScriptedActor is an Actor that follows a predefined script of actions.

    Attributes:
        script (list[ScriptKeyPoint]): The list of script key points to be executed.
    """
    script: list[ScriptKeyPoint] = []

    def update(self):
        """
        Updates the state of the ScriptedActor by executing actions from the script
        that are scheduled to occur before the current time.
        """
        while self.script:
            if self.script[0].timestamp >= datetime.now(tz=self.script[0].timestamp.tzinfo):
                break
            next_key_point = self.script.pop(0)
            action = self.get_action(next_key_point.action)
            if action:
                yield from action(*next_key_point.args, **next_key_point.kwargs)
        yield from super().update()
