import unittest
from datetime import datetime, timezone
from datetime import timedelta

from parameterized import parameterized

from relative_world.time import time_as_relative_string
from relative_world.time import utcnow


class TestTimeFunctions(unittest.TestCase):

    def test_utcnow_is_aware(self):
        """Test that utcnow returns an aware datetime object."""
        now = utcnow()
        self.assertTrue(
            now.tzinfo is not None and now.tzinfo.utcoffset(now) is not None,
            "utcnow should return an aware datetime object",
        )

    def test_utcnow_is_utc(self):
        """Test that utcnow returns a datetime object in UTC."""
        now = utcnow()
        self.assertEqual(
            now.tzinfo, timezone.utc, "utcnow should return a datetime object in UTC"
        )


class TestTimeAsRelativeString(unittest.TestCase):

    @parameterized.expand(
        [
            (
                    "just_now",
                    datetime.now() - timedelta(seconds=10),
                    datetime.now(),
                    "just now",
            ),
            (
                    "a_minute_ago",
                    datetime.now() - timedelta(minutes=1),
                    datetime.now(),
                    "a minute ago",
            ),
            (
                    "minutes_ago",
                    datetime.now() - timedelta(minutes=5),
                    datetime.now(),
                    "5 minutes ago",
            ),
            (
                    "an_hour_ago",
                    datetime.now() - timedelta(hours=1),
                    datetime.now(),
                    "an hour ago",
            ),
            (
                    "earlier_today",
                    datetime.now() - timedelta(hours=5),
                    datetime.now(),
                    "earlier today",
            ),
            (
                    "yesterday",
                    datetime.now() - timedelta(days=1),
                    datetime.now(),
                    "yesterday",
            ),
            (
                    "days_ago",
                    datetime.now() - timedelta(days=3),
                    datetime.now(),
                    "3 days ago",
            ),
            (
                    "last_week",
                    datetime.now() - timedelta(weeks=1),
                    datetime.now(),
                    "last week",
            ),
            (
                    "this_year",
                    datetime.now() - timedelta(days=200),
                    datetime.now(),
                    "this year",
            ),
            (
                    "a_year_ago",
                    datetime.now() - timedelta(days=365),
                    datetime.now(),
                    "a year ago",
            ),
            (
                    "years_ago",
                    datetime.now() - timedelta(days=365 * 5),
                    datetime.now(),
                    "5 years ago",
            ),
            (
                    "in_a_few_seconds",
                    datetime.now() + timedelta(seconds=10),
                    datetime.now(),
                    "in a few seconds",
            ),
            (
                    "in_a_minute",
                    datetime.now() + timedelta(minutes=1, seconds=1),
                    datetime.now(),
                    "in a minute",
            ),
            (
                    "in_minutes",
                    datetime.now() + timedelta(minutes=5, seconds=1),
                    datetime.now(),
                    "in 5 minutes",
            ),
            (
                    "in_an_hour",
                    datetime.now() + timedelta(hours=1, seconds=1),
                    datetime.now(),
                    "in an hour",
            ),
            (
                    "in_hours",
                    datetime.now() + timedelta(hours=5, seconds=1),
                    datetime.now(),
                    "in 5 hours",
            ),
            (
                    "tomorrow",
                    datetime.now() + timedelta(days=1, seconds=1),
                    datetime.now(),
                    "tomorrow",
            ),
            (
                    "in_days",
                    datetime.now() + timedelta(days=3, seconds=1),
                    datetime.now(),
                    "in 3 days",
            ),
            (
                    "next_week",
                    datetime.now() + timedelta(weeks=1, seconds=1),
                    datetime.now(),
                    "next week",
            ),
            (
                    "later_this_year",
                    datetime.now() + timedelta(days=200, seconds=1),
                    datetime.now(),
                    "later this year",
            ),
            (
                    "next_year",
                    datetime.now() + timedelta(days=365, seconds=1),
                    datetime.now(),
                    "next year",
            ),
            (
                    "in_years",
                    datetime.now() + timedelta(days=365 * 5, seconds=1),
                    datetime.now(),
                    "in 5 years",
            ),
        ]
    )
    def test_time_as_relative_string(self, _, start, end, expected):
        result = time_as_relative_string(start, end)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
