"""Timestamp helpers for memory models."""

from __future__ import annotations

from datetime import datetime, timezone


def utc_now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string with a Z suffix."""

    return format_utc_timestamp(datetime.now(timezone.utc))


def format_utc_timestamp(value: datetime) -> str:
    """Format a datetime as a UTC ISO 8601 string with a Z suffix."""

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
