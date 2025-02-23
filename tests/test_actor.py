import pytest
import asyncio
import uuid

from relative_world.actor import Actor
from relative_world.world import RelativeWorld
from relative_world.location import Location
from relative_world.event import Event
from relative_world.entity import BoundEvent


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio(scope="session")
async def test_initialization():
    world = RelativeWorld()
    actor = Actor(world=world)
    assert actor.world == world, "Actor should be initialized with the correct world"
    assert actor.location_id is None, "Actor should have no location initially"


@pytest.mark.asyncio(scope="session")
async def test_set_world():
    world = RelativeWorld()
    new_world = RelativeWorld()
    actor = Actor(world=world)
    actor.world = new_world
    assert actor.world == new_world, "Actor's world should be updated"
    assert actor.location_id == new_world.id, "Actor's location_id should be the new world"


@pytest.mark.asyncio(scope="session")
async def test_set_location():
    world = RelativeWorld()
    location = Location(id=uuid.uuid4())
    actor = Actor(world=world)
    world.add_location(location)
    actor.location = location
    assert actor.location_id == location.id, "Actor's location_id should be set correctly"
    assert actor.location == location, "Actor's location should be set correctly"


@pytest.mark.asyncio(scope="session")
async def test_update():
    world = RelativeWorld()
    actor = Actor(world=world)
    events = [event async for event in actor.update()]
    assert events == [], "Update should yield no events by default"


@pytest.mark.asyncio(scope="session")
async def test_act():
    world = RelativeWorld()
    actor = Actor(world=world)
    events = [event async for event in actor.act()]
    assert events == [], "Act should yield no events by default"


@pytest.mark.asyncio(scope="session")
async def test_emit_event():
    world = RelativeWorld()
    actor = Actor(world=world)
    event = Event(type="SAY_ALOUD", context={})
    actor.emit_event(event)

    events = [event async for event in actor.pop_event_batch_iterator()]
    assert len(events) == 1, "emit_event should add one event to the batch"
    assert events[0][1] == event, "The emitted event should be in the batch"


@pytest.mark.asyncio(scope="session")
async def test_handle_event():
    world = RelativeWorld()
    location = Location(id=uuid.uuid4())
    actor = Actor(world=world)
    world.add_location(location)
    actor.location = location

    event = Event(type="SAY_ALOUD", context={})
    await actor.handle_event(actor, event)
    assert actor.should_propagate_event(
        bound_event=(actor, event)
    ), "Event should be handled by actor"


@pytest.mark.asyncio(scope="session")
async def test_find_by_id():
    world = RelativeWorld()
    actor = Actor(world=world)
    location = Location(id=uuid.uuid4())
    world.add_location(location)
    actor.location = location

    found_entity = await actor.find_by_id(actor.id)
    assert found_entity == actor, "find_by_id should return the correct actor entity"


@pytest.mark.asyncio(scope="session")
async def test_clear_event_handler():
    world = RelativeWorld()
    actor = Actor(world=world)
    event_type = Event
    handler = lambda entity, event: None

    actor.set_event_handler(event_type, handler)
    assert event_type in actor._event_handlers, "Event handler should be set"

    actor.clear_event_handler(event_type)
    assert event_type not in actor._event_handlers, "Event handler should be cleared"


@pytest.mark.asyncio(scope="session")
async def test_pop_event_batch_iterator():
    world = RelativeWorld()
    actor = Actor(world=world)
    event = Event(type="SAY_ALOUD", context={})
    actor.emit_event(event)

    events = [event async for event in actor.pop_event_batch_iterator()]
    assert len(events) == 1, "pop_event_batch_iterator should yield one event"
    assert events[0][1] == event, "The yielded event should be the emitted event"

    # Ensure the batch is cleared after popping
    events = [event async for event in actor.pop_event_batch_iterator()]
    assert len(events) == 0, "The event batch should be empty after popping"


@pytest.mark.asyncio(scope="session")
async def test_event_handler_registration_and_calling():
    world = RelativeWorld()
    actor = Actor(world=world)
    event_type = Event
    handler_called = False

    async def handler(entity, event):
        nonlocal handler_called
        handler_called = True

    actor.set_event_handler(event_type, handler)
    assert event_type in actor._event_handlers, "Event handler should be registered"

    event = Event(type="SAY_ALOUD", context={})
    await actor.handle_event(actor, event)
    assert handler_called, "Event handler should be called when event is handled"