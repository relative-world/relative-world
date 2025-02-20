import uuid
from typing import Annotated

from pydantic import PrivateAttr

from relative_world.entity import Entity
from relative_world.location import Location
from relative_world.world import RelativeWorld

class Actor(Entity):
    """
    Represents an actor within a relative world.

    Attributes
    ----------
    _world : RelativeWorld | None
        The world in which the actor exists.
    location_id : uuid.UUID
        The unique identifier for the actor's location.

    Parameters
    ----------
    world : RelativeWorld | None, optional
        The world in which the actor exists.
    data : dict, optional
        Additional data for the actor.
    """

    _world: Annotated[RelativeWorld | None, PrivateAttr()]
    location_id: uuid.UUID

    def __init__(self, *, world=None, **data):
        """
        Initializes a new actor.

        Parameters
        ----------
        world : RelativeWorld | None, optional
            The world in which the actor exists.
        data : dict, optional
            Additional data for the actor.
        """
        super().__init__(**data)
        self._world = world

    @property
    def world(self):
        """
        Gets the world in which the actor exists.

        Returns
        -------
        RelativeWorld | None
            The world in which the actor exists.
        """
        return self._world

    @world.deleter
    def world(self):
        """
        Deletes the world in which the actor exists.
        """
        self._world.remove_entity(self)
        self._world = None

    @world.setter
    def world(self, value):
        """
        Sets the world in which the actor exists.

        Parameters
        ----------
        value : RelativeWorld
            The new world for the actor.
        """
        if self._world:
            del self.world
        self._world = value
        self._world.add_entity(self)
        self.location_id = self._world.id

    @property
    def location(self) -> Location | None:
        """
        Gets the location of the actor within the world.

        Returns
        -------
        Location | None
            The location of the actor.
        """
        return self.world.get_location_by_id(self.location_id)

    @location.setter
    def location(self, value):
        """
        Sets the location of the actor within the world.

        Parameters
        ----------
        value : Location
            The new location for the actor.
        """
        self.location_id = value.id
