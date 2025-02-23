import pytest
from relative_world.entity import Entity
from relative_world.event import Event
from relative_world.location import Location


class ExampleEntity(Entity):
    def should_propagate_event(self, entity, event: Event) -> bool:
        return True


class ExampleCancellingEntity(Entity):
    def should_propagate_event(self, entity, event: Event) -> bool:
        return False


@pytest.mark.asyncio(scope="session")
async def test_propagate_event_private():
    parent = Location(private=True)
    child = ExampleEntity()
    parent.children = [child]

    event = Event(type="SAY_ALOUD", context={})
    result = parent.should_propagate_event(bound_event=(parent, event))
    assert not result, "Event should not propagate because location is private"


@pytest.mark.asyncio(scope="session")
async def test_propagate_event_not_private():
    parent = Location(private=False)
    child = ExampleEntity()
    parent.children = [child]

    event = Event(type="SAY_ALOUD", context={})
    result = parent.should_propagate_event(bound_event=(parent, event))
    assert result, "Event should propagate because location is not private"