from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import paginate_events


def _event(event_id: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def _query(filters: dict[str, object] | None = None, limit: int = 2) -> RecallQuery:
    return RecallQuery(
        query_id="query-001",
        query_text="task",
        requested_at="2026-06-14T10:01:00Z",
        limit=limit,
        filters={} if filters is None else filters,
    )


def test_paginate_events_defaults_to_query_limit() -> None:
    first = _event("event-001")
    second = _event("event-002")
    third = _event("event-003")

    assert paginate_events((first, second, third), _query(limit=2)) == (first, second)


def test_paginate_events_uses_offset_and_page_size() -> None:
    first = _event("event-001")
    second = _event("event-002")
    third = _event("event-003")

    assert paginate_events(
        (first, second, third),
        _query({"offset": 1, "page_size": 1}),
    ) == (second,)


def test_paginate_events_clamps_negative_offset() -> None:
    event = _event("event-001")

    assert paginate_events((event,), _query({"offset": -5})) == (event,)


def test_paginate_events_returns_empty_for_non_positive_page_size() -> None:
    assert paginate_events((_event("event-001"),), _query({"page_size": 0})) == ()
