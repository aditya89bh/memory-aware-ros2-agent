from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallResult,
    TaskTrace,
)
from memory_aware_ros2_agent.storage_queries import (
    events_by_type,
    latest_events,
    recall_results_after,
    traces_by_task_name,
)


def _event(
    event_id: str,
    event_type: EventType,
    timestamp: str,
    trace_id: str = "trace-001",
) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=event_type,
        timestamp=timestamp,
        summary="Task event.",
    )


def test_events_by_type_filters_by_type_and_trace() -> None:
    store = InMemoryStore()
    first = _event("event-001", EventType.TASK_STARTED, "2026-06-14T10:00:00Z")
    second = _event("event-002", EventType.TASK_STARTED, "2026-06-14T10:01:00Z", "x")
    third = _event("event-003", EventType.TASK_FAILED, "2026-06-14T10:02:00Z")
    store.save_event(first)
    store.save_event(second)
    store.save_event(third)

    assert events_by_type(store, EventType.TASK_STARTED, "trace-001") == (first,)


def test_latest_events_returns_newest_events() -> None:
    store = InMemoryStore()
    first = _event("event-001", EventType.TASK_STARTED, "2026-06-14T10:00:00Z")
    second = _event("event-002", EventType.TASK_FAILED, "2026-06-14T10:02:00Z")
    third = _event("event-003", EventType.TASK_SUCCEEDED, "2026-06-14T10:01:00Z")
    store.save_event(first)
    store.save_event(second)
    store.save_event(third)

    assert latest_events(store, 2) == (second, third)
    assert latest_events(store, 0) == ()


def test_traces_by_task_name_filters_trace_names() -> None:
    store = InMemoryStore()
    first = TaskTrace("trace-001", "inspect", "2026-06-14T10:00:00Z")
    second = TaskTrace("trace-002", "dock", "2026-06-14T10:01:00Z")
    store.save_trace(first)
    store.save_trace(second)

    assert traces_by_task_name(store, "inspect") == (first,)


def test_recall_results_after_filters_generated_at() -> None:
    store = InMemoryStore()
    first = RecallResult("query-001", generated_at="2026-06-14T10:00:00Z")
    second = RecallResult("query-002", generated_at="2026-06-14T10:01:00Z")
    missing = RecallResult("query-003")
    store.save_recall_result(first)
    store.save_recall_result(second)
    store.save_recall_result(missing)

    assert recall_results_after(store, "2026-06-14T10:01:00Z") == (second,)
