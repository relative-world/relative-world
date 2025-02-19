import unittest
from datetime import datetime, timezone
from relative_world.time import utcnow

class TestTimeFunctions(unittest.TestCase):

    def test_utcnow_is_aware(self):
        """Test that utcnow returns an aware datetime object."""
        now = utcnow()
        self.assertTrue(now.tzinfo is not None and now.tzinfo.utcoffset(now) is not None, "utcnow should return an aware datetime object")

    def test_utcnow_is_utc(self):
        """Test that utcnow returns a datetime object in UTC."""
        now = utcnow()
        self.assertEqual(now.tzinfo, timezone.utc, "utcnow should return a datetime object in UTC")

if __name__ == "__main__":
    unittest.main()
