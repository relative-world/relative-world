import pytest
from datetime import datetime, timezone, timedelta
from parameterized import parameterized
from relative_world.time import time_as_relative_string, utcnow


@pytest.mark.asyncio(scope="session")
async def test_utcnow_is_aware():
    """Test that utcnow returns an aware datetime object."""
    now = utcnow()
    assert now.tzinfo is not None and now.tzinfo.utcoffset(now) is not None, "utcnow should return an aware datetime object"


@pytest.mark.asyncio(scope="session")
async def test_utcnow_is_utc():
    """Test that utcnow returns a datetime object in UTC."""
    now = utcnow()
    assert now.tzinfo == timezone.utc, "utcnow should return a datetime object in UTC"


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (datetime.now() - timedelta(seconds=10), datetime.now(), "just now"),
        (datetime.now() - timedelta(minutes=1), datetime.now(), "a minute ago"),
        (datetime.now() - timedelta(minutes=5), datetime.now(), "5 minutes ago"),
        (datetime.now() - timedelta(hours=1), datetime.now(), "an hour ago"),
        (datetime.now() - timedelta(hours=5), datetime.now(), "earlier today"),
        (datetime.now() - timedelta(days=1), datetime.now(), "yesterday"),
        (datetime.now() - timedelta(days=3), datetime.now(), "3 days ago"),
        (datetime.now() - timedelta(weeks=1), datetime.now(), "last week"),
        (datetime.now() - timedelta(days=200), datetime.now(), "this year"),
        (datetime.now() - timedelta(days=365), datetime.now(), "a year ago"),
        (datetime.now() - timedelta(days=365 * 5), datetime.now(), "5 years ago"),
        (datetime.now() + timedelta(seconds=10), datetime.now(), "in a few seconds"),
        (datetime.now() + timedelta(minutes=1, seconds=1), datetime.now(), "in a minute"),
        (datetime.now() + timedelta(minutes=5, seconds=1), datetime.now(), "in 5 minutes"),
        (datetime.now() + timedelta(hours=1, seconds=1), datetime.now(), "in an hour"),
        (datetime.now() + timedelta(hours=5, seconds=1), datetime.now(), "in 5 hours"),
        (datetime.now() + timedelta(days=1, seconds=1), datetime.now(), "tomorrow"),
        (datetime.now() + timedelta(days=3, seconds=1), datetime.now(), "in 3 days"),
        (datetime.now() + timedelta(weeks=1, seconds=1), datetime.now(), "next week"),
        (datetime.now() + timedelta(days=200, seconds=1), datetime.now(), "later this year"),
        (datetime.now() + timedelta(days=365, seconds=1), datetime.now(), "next year"),
        (datetime.now() + timedelta(days=365 * 5, seconds=1), datetime.now(), "in 5 years"),
    ]
)
@pytest.mark.asyncio(scope="session")
async def test_time_as_relative_string(start, end, expected):
    result = time_as_relative_string(start, end)
    assert result == expected, f"Expected '{expected}', but got '{result}'"
