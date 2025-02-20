from datetime import datetime, timedelta, timezone


def utcnow():
    """
    Get the current UTC time.

    Returns
    -------
    datetime
        The current UTC time.
    """
    return datetime.now(timezone.utc)


def time_as_relative_string(start: datetime, end: datetime) -> str:
    """
    Returns the delta time from start to end as a string relative to the present.

    Examples
    --------
    "in 5 minutes", "5 minutes ago", "last week", "last month", "a year ago", "5 years ago"

    Parameters
    ----------
    start : datetime
        The start time.
    end : datetime
        The end time.

    Returns
    -------
    str
        The relative time as a string.
    """
    delta = end - start
    if start > end:
        delta = -delta
        if delta < timedelta(seconds=60):
            return "in a few seconds"
        if delta < timedelta(minutes=2):
            return "in a minute"
        if delta < timedelta(minutes=60):
            return f"in {delta.seconds // 60} minutes"
        if delta < timedelta(hours=2):
            return "in an hour"
        if delta < timedelta(hours=24):
            return f"in {delta.seconds // 3600} hours"
        if delta < timedelta(days=2):
            return "tomorrow"
        if delta < timedelta(days=7):
            return f"in {delta.days} days"
        if delta < timedelta(days=30):
            return "next week"
        if delta < timedelta(days=365):
            return "later this year"
        if delta < timedelta(days=365 * 2):
            return "next year"
        else:
            return f"in {delta.days // 365} years"
    else:
        if delta < timedelta(seconds=60):
            return "just now"
        if delta < timedelta(minutes=2):
            return "a minute ago"
        if delta < timedelta(minutes=60):
            return f"{delta.seconds // 60} minutes ago"
        if delta < timedelta(hours=2):
            return "an hour ago"
        if delta < timedelta(hours=24):
            return "earlier today"
        if delta < timedelta(days=2):
            return "yesterday"
        if delta < timedelta(days=7):
            return f"{delta.days} days ago"
        if delta < timedelta(days=30):
            return "last week"
        if delta < timedelta(days=365):
            return "this year"
        if delta < timedelta(days=365 * 2):
            return "a year ago"
        else:
            return f"{delta.days // 365} years ago"
