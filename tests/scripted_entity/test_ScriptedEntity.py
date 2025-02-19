import unittest
from datetime import datetime, timedelta, timezone

from relative_world.scripted_entity import ScriptedEntity, ScriptKeyPoint


class EchoEntity(ScriptedEntity):
    script: list[ScriptKeyPoint] = []

    def get_action(self, action):
        if action == "echo":
            return self.echo

    def echo(self, message=""):
        return f"Echo: {message}"


class TestScriptedEntity(unittest.TestCase):
    def test_no_script(self):
        actor = EchoEntity()
        actor.update()
        self.assertEqual(len(actor.script), 0)

    def test_single_action_executes(self):
        now = datetime.now(tz=timezone.utc)
        actor = EchoEntity(
            script=[
                ScriptKeyPoint(timestamp=now, action="echo", args=["Test"], kwargs={})
            ]
        )
        for _ in actor.update():
            continue
        self.assertEqual(len(actor.script), 0)

    def test_future_action_skips(self):
        actor = EchoEntity()
        future_time = datetime.now() + timedelta(seconds=5)
        actor.script = [
            ScriptKeyPoint(
                timestamp=future_time, action="echo", args=["Future"], kwargs={}
            )
        ]
        actor.update()
        self.assertEqual(len(actor.script), 1)

    def test_multiple_actions(self):
        now = datetime.now(tz=timezone.utc)
        past_time = now - timedelta(seconds=1)
        future_time = now + timedelta(seconds=5)
        actor = EchoEntity(
            script=[
                ScriptKeyPoint(
                    timestamp=past_time, action="echo", args=["Past"], kwargs={}
                ),
                ScriptKeyPoint(
                    timestamp=now, action="echo", args=["Immediate"], kwargs={}
                ),
                ScriptKeyPoint(
                    timestamp=future_time, action="echo", args=["Future"], kwargs={}
                ),
            ]
        )
        for _ in actor.update():
            continue
        self.assertEqual(1, len(actor.script))
        self.assertEqual(
            ["Future"],
            actor.script[0].args,
        )

    def test_action_with_kwargs(self):
        actor = EchoEntity()
        now = datetime.now()
        actor.script = [
            ScriptKeyPoint(
                timestamp=now,
                action="echo",
                args=[],
                kwargs={"message": "Test with kwargs"},
            )
        ]
        for _ in actor.update():
            continue
        self.assertEqual(0, len(actor.script))

    def test_past_action_executes(self):
        actor = EchoEntity()
        past_time = datetime.now() - timedelta(seconds=5)
        actor.script = [
            ScriptKeyPoint(timestamp=past_time, action="echo", args=["Past"], kwargs={})
        ]
        for _ in actor.update():
            continue
        self.assertEqual(0, len(actor.script))

    def test_empty_script(self):
        actor = EchoEntity()
        actor.script = []
        for _ in actor.update():
            continue
        self.assertEqual(0, len(actor.script))

    def test_action_with_no_args_or_kwargs(self):
        actor = EchoEntity()
        now = datetime.now()
        actor.script = [
            ScriptKeyPoint(timestamp=now, action="echo", args=[], kwargs={})
        ]
        for _ in actor.update():
            continue
        self.assertEqual(0, len(actor.script))


if __name__ == "__main__":
    unittest.main()
