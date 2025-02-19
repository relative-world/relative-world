import unittest
from relative_world.entity import Entity
from relative_world.events import BoundEvent


class ExampleEntity(Entity):
    def handle_event(self, event: BoundEvent) -> bool:
        return True


class ExampleCancellingEntity(Entity):
    def handle_event(self, event: BoundEvent) -> bool:
        return False


class TestEntity(unittest.TestCase):

    def test_handle_event_propagation(self):
        parent = Entity()
        child1 = ExampleEntity()
        child2 = ExampleCancellingEntity()
        parent.children = [child1, child2]

        event = BoundEvent(source_entity=parent)
        result = parent.handle_event(event)
        self.assertFalse(
            result, "Event should not propagate because one child cancels it"
        )

    def test_handle_event_all_propagate(self):
        parent = Entity()
        child1 = ExampleEntity()
        child2 = ExampleEntity()
        parent.children = [child1, child2]

        event = BoundEvent(source_entity=parent)
        result = parent.handle_event(event)
        self.assertTrue(result, "Event should propagate because all children allow it")

    def test_update(self):
        parent = Entity()
        child = ExampleEntity()
        parent.children = [child]

        events = list(parent.update())
        self.assertEqual(
            events,
            [],
            "Update should yield no events because ExampleEntity does not generate events",
        )

    def test_update_yields_events(self):
        class EventGeneratingEntity(Entity):
            def update(self):
                yield BoundEvent(source_entity=self)

        parent = Entity()
        child = EventGeneratingEntity()
        parent.children = [child]

        events = list(parent.update())
        self.assertEqual(len(events), 1, "Update should yield one event")
        self.assertIsInstance(
            events[0], BoundEvent, "Yielded event should be an instance of BoundEvent"
        )
        self.assertEqual(
            events[0].source_entity,
            child,
            "The source entity of the yielded event should be the child entity",
        )


if __name__ == "__main__":
    unittest.main()
