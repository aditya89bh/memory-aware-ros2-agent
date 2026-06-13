"""Factory helpers for memory models."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.id_utils import new_event_id
from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.time_utils import utc_now_iso


def create_memory_event(
    *,
    trace_id: str,
    event_type: EventType,
    summary: str,
    event_id: str | None = None,
    timestamp: str | None = None,
    payload: dict[str, Any] | None = None,
) -> MemoryEvent:
    """Create a memory event with generated defaults."""

    return MemoryEvent(
        event_id=event_id or new_event_id(),
        trace_id=trace_id,
        event_type=event_type,
        timestamp=timestamp or utc_now_iso(),
        summary=summary,
        payload=payload or {},
    )
