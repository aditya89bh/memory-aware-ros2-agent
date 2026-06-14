"""Deterministic load testing fixtures."""

from __future__ import annotations

from memory_aware_ros2_agent.factories import (
    create_memory_event,
    create_recall_query,
    create_task_trace,
)
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallQuery,
    TaskTrace,
)


def make_load_events(trace_id: str, count: int) -> tuple[MemoryEvent, ...]:
    """Create deterministic events for load tests."""

    return tuple(
        create_memory_event(
            trace_id=trace_id,
            event_type=EventType.TASK_OBSERVED,
            summary=f"Load observation {index}",
            event_id=f"{trace_id}-event-{index}",
            timestamp=f"2026-06-14T10:{index // 60:02d}:{index % 60:02d}Z",
            payload={"index": index, "scenario": "load"},
        )
        for index in range(count)
    )


def make_load_trace(
    *, trace_id: str = "trace-load", task_name: str = "load-test", event_count: int
) -> TaskTrace:
    """Create a deterministic trace for load tests."""

    return create_task_trace(
        trace_id=trace_id,
        task_name=task_name,
        started_at="2026-06-14T10:00:00Z",
        events=make_load_events(trace_id, event_count),
        ended_at=f"2026-06-14T10:{event_count // 60:02d}:{event_count % 60:02d}Z",
    )


def make_load_store(event_count: int) -> InMemoryStore:
    """Create an in-memory store populated with load fixture data."""

    store = InMemoryStore()
    trace = make_load_trace(event_count=event_count)
    store.save_trace(trace)
    for event in trace.events:
        store.save_event(event)
    return store


def make_load_recall_query(
    *, query_id: str = "query-load", limit: int = 10
) -> RecallQuery:
    """Create a recall query suitable for load fixture data."""

    return create_recall_query(
        query_id=query_id,
        query_text="load observation",
        trace_id="trace-load",
        limit=limit,
    )
