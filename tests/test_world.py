import pytest
from relative_world.world import RelativeWorld
from relative_world.location import Location


@pytest.mark.asyncio(scope="session")
async def test_initial_time_step():
    relative_world = RelativeWorld()
    assert relative_world.previous_iterations == 0, "Initial previous_iterations should be 0"


@pytest.mark.asyncio(scope="session")
async def test_update():
    relative_world = RelativeWorld()
    relative_world.previous_iterations = 0
    await relative_world.step()
    assert relative_world.previous_iterations == 1, "Update should advance the simulation by one iteration"


@pytest.mark.asyncio(scope="session")
async def test_update_with_zero_time_step():
    relative_world = RelativeWorld()
    relative_world.previous_iterations = 1
    async for _ in relative_world.update():
        pass
    assert relative_world.previous_iterations == 2, "Update should still advance the simulation"


@pytest.mark.asyncio(scope="session")
async def test_update_with_negative_time_step():
    relative_world = RelativeWorld()
    async for _ in relative_world.update():
        pass
    assert relative_world.previous_iterations == 1, "Update should still advance the simulation"


@pytest.mark.asyncio(scope="session")
async def test_add_location():
    relative_world = RelativeWorld()
    location = Location()
    relative_world.add_location(location)
    assert location.id in relative_world._locations, "Location should be added to the world"


@pytest.mark.asyncio(scope="session")
async def test_remove_location():
    relative_world = RelativeWorld()
    location = Location()
    relative_world.add_location(location)
    relative_world.remove_location(location)
    assert location.id not in relative_world._locations, "Location should be removed from the world"


@pytest.mark.asyncio(scope="session")
async def test_connect_locations():
    relative_world = RelativeWorld()
    location_a = Location()
    location_b = Location()
    relative_world.add_location(location_a)
    relative_world.add_location(location_b)
    relative_world.connect_locations(location_a.id, location_b.id)
    assert location_b.id in relative_world._connections[location_a.id], "Locations should be connected"
    assert location_a.id in relative_world._connections[location_b.id], "Locations should be connected"


@pytest.mark.asyncio(scope="session")
async def test_get_connected_locations():
    relative_world = RelativeWorld()
    location_a = Location()
    location_b = Location()
    relative_world.add_location(location_a)
    relative_world.add_location(location_b)
    relative_world.connect_locations(location_a.id, location_b.id)
    connected_locations = relative_world.get_connected_locations(location_a.id)
    assert location_b in connected_locations, "Should return connected locations"


@pytest.mark.asyncio(scope="session")
async def test_iter_locations():
    relative_world = RelativeWorld()
    location = Location()
    relative_world.add_location(location)
    locations = [loc async for loc in relative_world.iter_locations()]
    assert location in locations, "Should iterate over all locations in the world"