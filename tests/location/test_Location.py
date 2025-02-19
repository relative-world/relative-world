import unittest
from relative_world.entity import Entity
from relative_world.event import Event, EventType
from relative_world.location import Location


class ExampleEntity(Entity):
    def propagate_event(self, entity, event: Event) -> bool:
        return True


class ExampleCancellingEntity(Entity):
    def propagate_event(self, entity, event: Event) -> bool:
        return False


class TestLocation(unittest.TestCase):

    def test_propagate_event_private(self):
        parent = Location(private=True)
        child = ExampleEntity()
        parent.children = [child]

        event = Event(type=EventType.SAY_ALOUD, context={})
        result = parent.propagate_event(parent, event)
        self.assertFalse(result, "Event should not propagate because location is private")

    def test_propagate_event_not_private(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.children = [child]

        event = Event(type=EventType.SAY_ALOUD, context={})
        result = parent.propagate_event(parent, event)
        self.assertTrue(result, "Event should propagate because location is not private")

    def test_propagate_event_child_cancels(self):
        parent = Location(private=False)
        child = ExampleCancellingEntity()
        parent.children = [child]

        event = Event(type=EventType.SAY_ALOUD, context={})
        result = parent.propagate_event(parent, event)
        self.assertFalse(result, "Event should not propagate because child cancels it")


if __name__ == "__main__":
    unittest.main()
