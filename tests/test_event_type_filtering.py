from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import (
    event_types_from_query,
    filter_events_by_query_event_types,
)


def _event(event_id: str, event_type: EventType) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def _query(event_types: object | None = None) -> RecallQuery:
    filters = {} if event_types is None else {"event_types": event_types}
    return RecallQuery(
        query_id="query-001",
        query_text="task",
        requested_at="2026-06-14T10:01:00Z",
        filters=filters,
    )


def test_event_types_from_query_reads_single_event_type() -> None:
    assert event_types_from_query(_query("task.failed")) == (EventType.TASK_FAILED,)


def test_filter_events_by_query_event_types_keeps_allowed_types() -> None:
    started = _event("event-001", EventType.TASK_STARTED)
    failed = _event("event-002", EventType.TASK_FAILED)

    result = filter_events_by_query_event_types(
        (started, failed),
        _query(("task.started", "task.failed")),
    )

    assert result == (started, failed)


def test_filter_events_by_query_event_types_filters_disallowed_types() -> None:
    started = _event("event-001", EventType.TASK_STARTED)
    failed = _event("event-002", EventType.TASK_FAILED)

    result = filter_events_by_query_event_types(
        (started, failed),
        _query(("task.failed",)),
    )

    assert result == (failed,)


def test_filter_events_by_query_event_types_noops_without_filter() -> None:
    event = _event("event-001", EventType.TASK_STARTED)

    assert filter_events_by_query_event_types((event,), _query()) == (event,)
