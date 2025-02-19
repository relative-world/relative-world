from datetime import datetime
from typing import Any

from pydantic import BaseModel

from relative_world.entity import Entity


class ScriptKeyPoint(BaseModel):
    """
    ScriptKeyPoint represents a key point in a script for a ScriptedEntity.

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


class ScriptedEntity(Entity):
    """
    ScriptedActor is an Actor that follows a predefined script of actions.

    Attributes:
        script (list[ScriptKeyPoint]): The list of script key points to be executed.
    """

    script: list[ScriptKeyPoint] = []

    def get_action(self, action: str):
        """
        Retrieves the action method corresponding to the given action name.

        Args:
            action (str): The name of the action to retrieve.

        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError

    def update(self):
        """
        Updates the state of the ScriptedEntity by executing actions from the script
        that are scheduled to occur before the current time.
        """
        while self.script and self.script[0].timestamp <= datetime.now(
            tz=self.script[0].timestamp.tzinfo
        ):
            next_key_point = self.script.pop(0)
            action = self.get_action(next_key_point.action)
            if action:
                yield from action(*next_key_point.args, **next_key_point.kwargs) or []
        yield from super().update()
