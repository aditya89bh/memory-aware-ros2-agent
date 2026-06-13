"""Factory helpers for memory models."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.id_utils import new_event_id, new_query_id, new_trace_id
from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery, TaskTrace
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


def create_task_trace(
    *,
    task_name: str,
    trace_id: str | None = None,
    started_at: str | None = None,
    events: tuple[MemoryEvent, ...] = (),
    ended_at: str | None = None,
) -> TaskTrace:
    """Create a task trace with generated defaults."""

    return TaskTrace(
        trace_id=trace_id or new_trace_id(),
        task_name=task_name,
        started_at=started_at or utc_now_iso(),
        events=events,
        ended_at=ended_at,
    )


def create_recall_query(
    *,
    query_text: str,
    query_id: str | None = None,
    requested_at: str | None = None,
    trace_id: str | None = None,
    limit: int = 5,
    filters: dict[str, Any] | None = None,
) -> RecallQuery:
    """Create a recall query with generated defaults."""

    return RecallQuery(
        query_id=query_id or new_query_id(),
        query_text=query_text,
        requested_at=requested_at or utc_now_iso(),
        trace_id=trace_id,
        limit=limit,
        filters=filters or {},
    )
