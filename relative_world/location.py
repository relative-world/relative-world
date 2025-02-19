from relative_world.entity import Entity


class Location(Entity):
    """
    A location in the world.

    Private locations will not bubble events to their parents.
    """
    private: bool = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def propagate_event(self, entity, event) -> bool:
        downstream = super().propagate_event(entity, event)
        return not self.private and downstream

