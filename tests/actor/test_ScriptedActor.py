from datetime import datetime, timedelta
import unittest
from relative_world.actor import ScriptedActor, ScriptKeyPoint

class EchoActor(ScriptedActor):
    def get_action(self, action):
        if action == "echo":
            return self.echo
        raise NotImplementedError(f"Action '{action}' not recognized")

    def echo(self, message):
        return f"Echo: {message}"

class TestScriptedActor(unittest.TestCase):
    def test_no_script(self):
        actor = EchoActor()
        actor.update()
        self.assertEqual(len(actor.script), 0)

    def test_single_action_executes(self):
        actor = EchoActor()
        now = datetime.now()
        actor.script = [ScriptKeyPoint(timestamp=now, action="echo", args=["Test"], kwargs={})]
        actor.update()
        self.assertEqual(len(actor.script), 0)

    def test_future_action_skips(self):
        actor = EchoActor()
        future_time = datetime.now() + timedelta(seconds=5)
        actor.script = [ScriptKeyPoint(timestamp=future_time, action="echo", args=["Future"], kwargs={})]
        actor.update()
        self.assertEqual(len(actor.script), 1)

    def test_multiple_actions(self):
        actor = EchoActor()
        now = datetime.now()
        past_time = now - timedelta(seconds=1)
        future_time = now + timedelta(seconds=5)
        actor.script = [
            ScriptKeyPoint(timestamp=past_time, action="echo", args=["Past"], kwargs={}),
            ScriptKeyPoint(timestamp=now, action="echo", args=["Immediate"], kwargs={}),
            ScriptKeyPoint(timestamp=future_time, action="echo", args=["Future"], kwargs={})
        ]
        actor.update()
        self.assertEqual(len(actor.script), 1)
        self.assertEqual(actor.script[0].args, ["Future"])

if __name__ == '__main__':
    unittest.main()
