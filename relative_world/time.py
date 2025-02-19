from datetime import datetime, timedelta


def time_as_relative_string(start: datetime, end: datetime) -> str:
    """Returns the delta time from start to end as a string relative to the present.

    e.g. "in 5 minutes", "5 minutes ago", "last week", "last month", "a year ago", "5 years ago"

    The idea is that maybe LLMs can reason about these statements better than iso 8601 timestamps.
        (honestly... idk, trying things is about learning things)
    """
    delta = end - start
    if delta < timedelta(seconds=60):
        return "just now"
    if delta < timedelta(minutes=2):
        return "a minute ago"
    if delta < timedelta(minutes=60):
        return f"{delta.seconds // 60} minutes ago"
    if delta < timedelta(hours=2):
        return "an hour ago"
    if delta < timedelta(hours=24):
        return f"earlier today"
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
