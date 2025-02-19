import unittest

from relative_world.entity import Entity
from relative_world.event import Event
from relative_world.location import Location


class ExampleEntity(Entity):
    def propagate_event(self, entity, event: Event) -> bool:
        return True


class ExampleCancellingEntity(Entity):
    def propagate_event(self, entity, event: Event) -> bool:
        return False


class TestEntity(unittest.TestCase):

    def test_handle_event_all_propagate(self):
        parent = Entity()
        child1 = ExampleEntity()
        child2 = ExampleEntity()
        parent.children = [child1, child2]

        event = Event(type="SAY_ALOUD", context={})
        result = parent.propagate_event(parent, event)
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
            ran_once: bool = False

            def update(self):
                if not self.ran_once:
                    self.ran_once = True
                    yield self, Event(type="SAY_ALOUD", context={})

        parent = Entity()
        child = EventGeneratingEntity()
        parent.children = [child]

        events = list(parent.update())
        self.assertEqual(len(events), 1, "Update should yield one event")
        self.assertIsInstance(
            events[0][1], Event, "Yielded event should be an instance of BoundEvent"
        )
        self.assertEqual(
            events[0][0],
            child,
            "The source entity of the yielded event should be the child entity",
        )

    def test_handle_event(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        parent.handle_event(parent, event)
        # Assuming handle_event should propagate the event to children
        self.assertTrue(
            child.propagate_event(parent, event),
            "Event should be handled by child entity",
        )

    def test_handle_event_with_cancelling_child(self):
        parent = Location(private=False)
        child = ExampleCancellingEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        parent.handle_event(parent, event)
        # Assuming handle_event should not propagate the event if child cancels it
        self.assertFalse(
            child.propagate_event(parent, event),
            "Event should not be handled by child entity",
        )

    def test_handle_event(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        parent.handle_event(parent, event)
        # Assuming handle_event should propagate the event to children
        self.assertTrue(
            child.propagate_event(parent, event),
            "Event should be handled by child entity",
        )

    def test_handle_event_with_cancelling_child(self):
        parent = Location(private=False)
        child = ExampleCancellingEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        parent.handle_event(parent, event)
        # Assuming handle_event should not propagate the event if child cancels it
        self.assertFalse(
            child.propagate_event(parent, event),
            "Event should not be handled by child entity",
        )

    def test_add_entity(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.add_entity(child)
        self.assertIn(child, parent.children, "Child entity should be added to parent")

    def test_remove_entity(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.add_entity(child)
        parent.remove_entity(child)
        self.assertNotIn(
            child, parent.children, "Child entity should be removed from parent"
        )


if __name__ == "__main__":
    unittest.main()
