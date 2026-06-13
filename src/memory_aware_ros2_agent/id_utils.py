"""Identifier helpers for memory models."""

from __future__ import annotations

from uuid import uuid4


def new_id(prefix: str) -> str:
    """Create a compact UUID-backed identifier with a readable prefix."""

    normalized_prefix = prefix.strip().lower().replace("_", "-")
    if not normalized_prefix:
        msg = "Identifier prefix must not be empty"
        raise ValueError(msg)
    return f"{normalized_prefix}-{uuid4().hex}"


def new_event_id() -> str:
    """Create a memory event identifier."""

    return new_id("event")


def new_trace_id() -> str:
    """Create a task trace identifier."""

    return new_id("trace")


def new_query_id() -> str:
    """Create a recall query identifier."""

    return new_id("query")
