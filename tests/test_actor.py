import unittest
import uuid
from relative_world.actor import Actor
from relative_world.world import RelativeWorld
from relative_world.location import Location


class TestActor(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.world = RelativeWorld()
        self.location = Location(id=uuid.uuid4())
        self.actor = Actor(world=self.world)
        self.world.add_location(self.location)

    async def test_initialization(self):
        self.assertIsNone(self.actor.location_id)
        self.assertEqual(self.actor.world, self.world)

    async def test_set_world(self):
        new_world = RelativeWorld()
        self.actor.world = new_world
        self.assertEqual(self.actor.world, new_world)
        self.assertEqual(self.actor.location_id, new_world.id)

    async def test_set_location(self):
        self.actor.world = self.world
        self.actor.location = self.location
        self.assertEqual(self.actor.location_id, self.location.id)
        self.assertEqual(self.actor.location, self.location)

    async def test_update(self):
        events = [event async for event in self.actor.update()]
        self.assertEqual(events, [])

    async def test_act(self):
        events = [event async for event in self.actor.act()]
        self.assertEqual(events, [])


if __name__ == "__main__":
    unittest.main()