import logging
from typing import Self

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Entity(BaseModel):
    """
    Entity is a base class for all entities in the simulation.

    Attributes:
        children (list[Self]): A list of child entities.
    """

    children: list[Self] = []

    def error_handler(self, exc):
        """
        Handles errors by logging the exception.

        Args:
            exc (Exception): The exception to handle.
        """
        logger.exception(exc_info=exc)

    def update(self):
        """
        Updates the state of the entity and its children.
        """
        for child in self.children:
            child.update()
