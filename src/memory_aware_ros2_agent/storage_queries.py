"""Query helpers for persistence stores."""

from __future__ import annotations

from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallResult,
    TaskTrace,
)
from memory_aware_ros2_agent.persistence import MemoryStore


def events_by_type(
    store: MemoryStore,
    event_type: EventType,
    trace_id: str | None = None,
) -> tuple[MemoryEvent, ...]:
    """Return events matching an event type."""

    return tuple(
        event
        for event in store.list_events(trace_id)
        if event.event_type == event_type
    )


def latest_events(store: MemoryStore, limit: int) -> tuple[MemoryEvent, ...]:
    """Return the newest events by timestamp."""

    if limit < 1:
        return ()
    events = sorted(
        store.list_events(),
        key=lambda event: event.timestamp,
        reverse=True,
    )
    return tuple(events[:limit])


def traces_by_task_name(store: MemoryStore, task_name: str) -> tuple[TaskTrace, ...]:
    """Return traces matching a task name."""

    return tuple(trace for trace in store.list_traces() if trace.task_name == task_name)


def recall_results_after(
    store: MemoryStore,
    generated_at: str,
) -> tuple[RecallResult, ...]:
    """Return recall results generated at or after a timestamp."""

    return tuple(
        result
        for result in store.list_recall_results()
        if result.generated_at is not None and result.generated_at >= generated_at
    )
