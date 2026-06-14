import pytest

from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import filter_events_by_query_metadata


def _event(event_id: str, payload: dict[str, object]) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
        payload=payload,
    )


def _query(metadata: object | None = None) -> RecallQuery:
    filters = {} if metadata is None else {"metadata": metadata}
    return RecallQuery(
        query_id="query-001",
        query_text="task",
        requested_at="2026-06-14T10:01:00Z",
        filters=filters,
    )


def test_filter_events_by_query_metadata_matches_payload_values() -> None:
    match = _event("event-001", {"zone": "dock", "priority": 2})
    miss = _event("event-002", {"zone": "lab", "priority": 2})

    result = filter_events_by_query_metadata(
        (match, miss),
        _query({"zone": "dock", "priority": 2}),
    )

    assert result == (match,)


def test_filter_events_by_query_metadata_noops_without_filter() -> None:
    event = _event("event-001", {"zone": "dock"})

    assert filter_events_by_query_metadata((event,), _query()) == (event,)


def test_filter_events_by_query_metadata_rejects_non_mapping() -> None:
    with pytest.raises(ValueError, match="mapping"):
        filter_events_by_query_metadata((), _query("zone=dock"))
