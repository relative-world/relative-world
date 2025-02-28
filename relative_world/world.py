import uuid
from typing import AsyncIterator, Annotated, Iterator

from pydantic import PrivateAttr

from relative_world.entity import BoundEvent
from relative_world.location import Location


class RelativeWorld(Location):
    previous_iterations: int = 0
    _locations: Annotated[dict[uuid.UUID, Location], PrivateAttr()] = {}
    _connections: Annotated[dict[uuid.UUID, set[uuid.UUID]], PrivateAttr()] = {}

    def add_location(self, location: Location):
        self._locations[location.id] = location
        if location.id not in self._connections:
            self._connections[location.id] = set()
        self.add_entity(location)

    def remove_location(self, location: Location):
        if location.id in self._locations:
            del self._locations[location.id]
        self.remove_entity(location)

    def get_location(self, location_id: uuid.UUID) -> Location:
        if location_id is self.id:
            return self
        return self._locations[location_id]

    def connect_locations(self, location_a: uuid.UUID, location_b: uuid.UUID) -> None:
        if location_a not in self._locations or location_b not in self._locations:
            raise ValueError("Both locations must exist in the world")

        self._connections[location_a].add(location_b)
        self._connections[location_b].add(location_a)

    def get_connected_locations(self, location_id: uuid.UUID) -> list[Location]:
        if location_id not in self._connections:
            return []
        return [self._locations[loc_id] for loc_id in self._connections[location_id]]

    def iter_locations(self) -> Iterator[Location]:
        for location in self.children:
            if isinstance(location, Location):
                yield location

    async def aiter_locations(self) -> AsyncIterator[Location]:
        for location in self.children:
            if isinstance(location, Location):
                yield location

    async def step(self):
        async for _ in self.update():
            pass
