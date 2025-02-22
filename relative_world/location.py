from relative_world.entity import Entity, BoundEvent


class Location(Entity):
    """
    A location in the world.

    Private locations will not bubble events to their parents.

    Attributes
    ----------
    private : bool
        Indicates whether the location is private. Private locations do not propagate events to their parents.
    """

    private: bool = True

    def __init__(self, *args, **kwargs):
        """
        Initialize a Location instance.

        Parameters
        ----------
        *args : tuple
            Variable length argument list.
        **kwargs : dict
            Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    def should_propagate_event(self, bound_event: BoundEvent) -> bool:
        """
        Propagate an event to the parent entity if the location is not private.

        Parameters
        ----------
        entity : Entity
            The entity that is propagating the event.
        event : Event
            The event to be propagated.

        Returns
        -------
        bool
            True if the event was propagated to the parent entity, False otherwise.
        """
        return not self.private

    def add_actor(self, actor):
        """
        Add an actor to the location.

        Parameters
        ----------
        actor : Actor
            The actor to be added to the location.
        """
        actor.location = self
        self.children.append(actor)
