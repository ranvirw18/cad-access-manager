"""
Date helpers — central place for the 50-day subscription rule.
"""

from datetime import date, timedelta

from config.settings import ACCESS_DAYS


def today() -> date:
    return date.today()


def expiry_from_join(join_date: date, days: int = ACCESS_DAYS) -> date:
    """expiry_date = join_date + 50 days"""
    return join_date + timedelta(days=days)


def is_expired(expiry_date: date, on_day: date | None = None) -> bool:
    """
    Subscription expired when today is AFTER expiry_date.
    On expiry_date itself, access is still allowed (last valid day).
    """
    check = on_day or today()
    return check > expiry_date


def days_remaining(expiry_date: date, on_day: date | None = None) -> int:
    """How many days left (0 if expired)."""
    check = on_day or today()
    remaining = (expiry_date - check).days
    return max(0, remaining)
