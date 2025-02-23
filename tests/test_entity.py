import pytest
import asyncio

from relative_world.entity import Entity, BoundEvent
from relative_world.event import Event
from relative_world.location import Location


class ExampleEntity(Entity):
    def should_propagate_event(self, bound_event: BoundEvent) -> bool:
        return True


class ExampleCancellingEntity(Entity):
    def should_propagate_event(self, bound_event: BoundEvent) -> bool:
        return False


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio(scope="session")
async def test_handle_event_all_propagate():
    parent = Entity()
    child1 = ExampleEntity()
    child2 = ExampleEntity()
    parent.children = [child1, child2]

    event = Event(type="SAY_ALOUD", context={})
    result = parent.should_propagate_event((parent, event))
    assert result, "Event should propagate because all children allow it"


@pytest.mark.asyncio(scope="session")
async def test_update():
    parent = Entity()
    child = ExampleEntity()
    parent.children = [child]

    events = [event async for event in parent.update()]
    assert (
        events == []
    ), "Update should yield no events because ExampleEntity does not generate events"


@pytest.mark.asyncio(scope="session")
async def test_update_yields_events():
    class EventGeneratingEntity(Entity):
        ran_once: bool = False

        async def update(self):
            if not self.ran_once:
                self.ran_once = True
                yield self, Event(type="SAY_ALOUD", context={})

    parent = Entity()
    child = EventGeneratingEntity()
    parent.children = [child]

    events = [event async for event in parent.update()]
    assert len(events) == 1, "Update should yield one event"
    assert isinstance(
        events[0][1], Event
    ), "Yielded event should be an instance of BoundEvent"
    assert (
        events[0][0] == child
    ), "The source entity of the yielded event should be the child entity"


@pytest.mark.asyncio(scope="session")
async def test_handle_event():
    parent = Location(private=False)
    child = ExampleEntity()
    parent.children = [child]

    event = Event(type="SAY_ALOUD", context={})
    await parent.handle_event(parent, event)
    assert child.should_propagate_event(
        bound_event=(parent, event)
    ), "Event should be handled by child entity"


@pytest.mark.asyncio(scope="session")
async def test_handle_event_with_cancelling_child():
    parent = Location(private=False)
    child = ExampleCancellingEntity()
    parent.children = [child]

    event = Event(type="SAY_ALOUD", context={})
    await parent.handle_event(parent, event)
    assert not child.should_propagate_event(
        bound_event=(parent, event)
    ), "Event should not be handled by child entity"


@pytest.mark.asyncio(scope="session")
async def test_add_entity():
    parent = Location(private=False)
    child = ExampleEntity()
    parent.add_entity(child)
    assert child in parent.children, "Child entity should be added to parent"


@pytest.mark.asyncio(scope="session")
async def test_remove_entity():
    parent = Location(private=False)
    child = ExampleEntity()
    parent.add_entity(child)
    parent.remove_entity(child)
    assert child not in parent.children, "Child entity should be removed from parent"


@pytest.mark.asyncio(scope="session")
async def test_find_by_id():
    parent = Entity()
    child = ExampleEntity()
    parent.add_entity(child)

    found_entity = await parent.find_by_id(child.id)
    assert found_entity == child, "find_by_id should return the correct child entity"


@pytest.mark.asyncio(scope="session")
async def test_emit_event():
    parent = Entity()
    event = Event(type="SAY_ALOUD", context={})
    parent.emit_event(event)

    events = [event async for event in parent.pop_event_batch_iterator()]
    assert len(events) == 1, "emit_event should add one event to the batch"
    assert events[0][1] == event, "The emitted event should be in the batch"


@pytest.mark.asyncio(scope="session")
async def test_clear_event_handler():
    parent = Entity()
    event_type = Event
    handler = lambda entity, event: None

    parent.set_event_handler(event_type, handler)
    assert event_type in parent._event_handlers, "Event handler should be set"

    parent.clear_event_handler(event_type)
    assert event_type not in parent._event_handlers, "Event handler should be cleared"


@pytest.mark.asyncio(scope="session")
async def test_pop_event_batch_iterator():
    parent = Entity()
    event = Event(type="SAY_ALOUD", context={})
    parent.emit_event(event)

    events = [event async for event in parent.pop_event_batch_iterator()]
    assert len(events) == 1, "pop_event_batch_iterator should yield one event"
    assert events[0][1] == event, "The yielded event should be the emitted event"

    # Ensure the batch is cleared after popping
    events = [event async for event in parent.pop_event_batch_iterator()]
    assert len(events) == 0, "The event batch should be empty after popping"


@pytest.mark.asyncio(scope="session")
async def test_event_handler_registration_and_calling():
    parent = Entity()
    event_type = Event
    handler_called = False

    async def handler(entity, event):
        nonlocal handler_called
        handler_called = True

    parent.set_event_handler(event_type, handler)
    assert event_type in parent._event_handlers, "Event handler should be registered"

    event = Event(type="SAY_ALOUD", context={})
    await parent.handle_event(parent, event)
    assert handler_called, "Event handler should be called when event is handled"


@pytest.mark.asyncio(scope="session")
async def test_propagate_event_false():
    class NonPropagatingEntity(Entity):
        def should_propagate_event(self, bound_event: BoundEvent) -> bool:
            return False

    grandparent = Entity()
    parent = Entity()
    child = NonPropagatingEntity()
    grandparent.add_entity(parent)
    parent.add_entity(child)

    event = Event(type="SAY_ALOUD", context={})
    child.emit_event(event)

    events = [event async for event in grandparent.update()]
    assert (
        len(events) == 1
    ), "Event should be received by the parent but not propagated to the grandparent"
    assert events[0][0] == child, "The event should be handled by the parent entity"
    assert events[0][1] == event, "The event should be the one emitted by the child"
    assert any(
        child.should_propagate_event((parent, event)) is False
        for child in parent.children
    ), "propagate_event should return False for the child entity"
