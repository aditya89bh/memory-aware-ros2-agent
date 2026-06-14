from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.persistence_api import (
    load_event,
    load_events_for_trace,
    persist_event,
)


def _event(event_id: str, trace_id: str = "trace-001") -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )


def test_persist_event_saves_and_returns_event() -> None:
    store = InMemoryStore()
    event = _event("event-001")

    result = persist_event(store, event)

    assert result == event
    assert load_event(store, "event-001") == event


def test_load_events_for_trace_filters_by_trace_id() -> None:
    store = InMemoryStore()
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-002")
    persist_event(store, first)
    persist_event(store, second)

    assert load_events_for_trace(store, "trace-001") == (first,)
