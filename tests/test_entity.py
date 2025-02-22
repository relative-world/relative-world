import unittest
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


class TestEntity(unittest.IsolatedAsyncioTestCase):

    async def test_handle_event_all_propagate(self):
        parent = Entity()
        child1 = ExampleEntity()
        child2 = ExampleEntity()
        parent.children = [child1, child2]

        event = Event(type="SAY_ALOUD", context={})
        result = parent.should_propagate_event((parent, event))
        self.assertTrue(result, "Event should propagate because all children allow it")

    async def test_update(self):
        parent = Entity()
        child = ExampleEntity()
        parent.children = [child]

        events = [event async for event in parent.update()]
        self.assertEqual(
            events,
            [],
            "Update should yield no events because ExampleEntity does not generate events",
        )

    async def test_update_yields_events(self):
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
        self.assertEqual(len(events), 1, "Update should yield one event")
        self.assertIsInstance(
            events[0][1], Event, "Yielded event should be an instance of BoundEvent"
        )
        self.assertEqual(
            events[0][0],
            child,
            "The source entity of the yielded event should be the child entity",
        )

    async def test_handle_event(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        await parent.handle_event(parent, event)
        self.assertTrue(
            child.should_propagate_event(bound_event=(parent, event)),
            "Event should be handled by child entity",
        )

    async def test_handle_event_with_cancelling_child(self):
        parent = Location(private=False)
        child = ExampleCancellingEntity()
        parent.children = [child]

        event = Event(type="SAY_ALOUD", context={})
        await parent.handle_event(parent, event)
        self.assertFalse(
            child.should_propagate_event(bound_event=(parent, event)),
            "Event should not be handled by child entity",
        )

    async def test_add_entity(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.add_entity(child)
        self.assertIn(child, parent.children, "Child entity should be added to parent")

    async def test_remove_entity(self):
        parent = Location(private=False)
        child = ExampleEntity()
        parent.add_entity(child)
        parent.remove_entity(child)
        self.assertNotIn(
            child, parent.children, "Child entity should be removed from parent"
        )

    async def test_find_by_id(self):
        parent = Entity()
        child = ExampleEntity()
        parent.add_entity(child)

        found_entity = await parent.find_by_id(child.id)
        self.assertEqual(
            found_entity, child, "find_by_id should return the correct child entity"
        )

    async def test_emit_event(self):
        parent = Entity()
        event = Event(type="SAY_ALOUD", context={})
        parent.emit_event(event)

        events = [event async for event in parent.pop_event_batch_iterator()]
        self.assertEqual(len(events), 1, "emit_event should add one event to the batch")
        self.assertEqual(
            events[0][1], event, "The emitted event should be in the batch"
        )

    async def test_clear_event_handler(self):
        parent = Entity()
        event_type = Event
        handler = lambda entity, event: None

        parent.set_event_handler(event_type, handler)
        self.assertIn(event_type, parent._event_handlers, "Event handler should be set")

        parent.clear_event_handler(event_type)
        self.assertNotIn(
            event_type, parent._event_handlers, "Event handler should be cleared"
        )

    async def test_pop_event_batch_iterator(self):
        parent = Entity()
        event = Event(type="SAY_ALOUD", context={})
        parent.emit_event(event)

        events = [event async for event in parent.pop_event_batch_iterator()]
        self.assertEqual(
            len(events), 1, "pop_event_batch_iterator should yield one event"
        )
        self.assertEqual(
            events[0][1], event, "The yielded event should be the emitted event"
        )

        # Ensure the batch is cleared after popping
        events = [event async for event in parent.pop_event_batch_iterator()]
        self.assertEqual(
            len(events), 0, "The event batch should be empty after popping"
        )

    async def test_event_handler_registration_and_calling(self):
        parent = Entity()
        event_type = Event
        handler_called = False

        async def handler(entity, event):
            nonlocal handler_called
            handler_called = True

        parent.set_event_handler(event_type, handler)
        self.assertIn(
            event_type, parent._event_handlers, "Event handler should be registered"
        )

        event = Event(type="SAY_ALOUD", context={})
        await parent.handle_event(parent, event)
        self.assertTrue(
            handler_called, "Event handler should be called when event is handled"
        )

    async def test_propagate_event_false(self):
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
        self.assertEqual(
            len(events),
            1,
            "Event should be received by the parent but not propagated to the grandparent",
        )
        self.assertEqual(
            events[0][0], child, "The event should be handled by the parent entity"
        )
        self.assertEqual(
            events[0][1], event, "The event should be the one emitted by the child"
        )
        self.assertTrue(
            any(
                child.should_propagate_event((parent, event)) is False
                for child in parent.children
            ),
            "propagate_event should return False for the child entity",
        )


if __name__ == "__main__":
    unittest.main()