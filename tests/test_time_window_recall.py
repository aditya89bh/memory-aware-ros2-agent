from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import (
    TimeWindowRecallEngine,
    filter_events_by_query_time_window,
)


def _event(event_id: str, timestamp: str, trace_id: str = "trace-001") -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary="Task event.",
    )


def _query(
    started_at: str | None = None,
    ended_at: str | None = None,
    trace_id: str | None = None,
) -> RecallQuery:
    filters = {}
    if started_at is not None:
        filters["started_at"] = started_at
    if ended_at is not None:
        filters["ended_at"] = ended_at
    return RecallQuery(
        query_id="query-001",
        query_text="task",
        requested_at="2026-06-14T10:03:00Z",
        trace_id=trace_id,
        filters=filters,
    )


def test_filter_events_by_query_time_window_uses_inclusive_bounds() -> None:
    before = _event("event-001", "2026-06-14T09:59:00Z")
    start = _event("event-002", "2026-06-14T10:00:00Z")
    end = _event("event-003", "2026-06-14T10:02:00Z")
    after = _event("event-004", "2026-06-14T10:03:00Z")

    result = filter_events_by_query_time_window(
        (before, start, end, after),
        _query("2026-06-14T10:00:00Z", "2026-06-14T10:02:00Z"),
    )

    assert result == (start, end)


def test_filter_events_by_query_time_window_noops_without_filters() -> None:
    event = _event("event-001", "2026-06-14T10:00:00Z")

    assert filter_events_by_query_time_window((event,), _query()) == (event,)


def test_time_window_recall_filters_store_events_and_trace() -> None:
    store = InMemoryStore()
    match = _event("event-001", "2026-06-14T10:01:00Z", "trace-001")
    wrong_trace = _event("event-002", "2026-06-14T10:01:00Z", "trace-002")
    store.save_event(match)
    store.save_event(wrong_trace)

    result = TimeWindowRecallEngine().recall(
        _query(started_at="2026-06-14T10:00:00Z", trace_id="trace-001"),
        store,
    )

    assert result.events == (match,)
    assert result.scores == (1.0,)
