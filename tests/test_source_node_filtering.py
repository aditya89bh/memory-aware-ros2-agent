from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import filter_events_by_query_source_nodes


def _event(event_id: str, source_node_id: str | None) -> MemoryEvent:
    payload = {} if source_node_id is None else {"source_node_id": source_node_id}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
        payload=payload,
    )


def _query(source_node_ids: object | None = None) -> RecallQuery:
    filters = {} if source_node_ids is None else {"source_node_ids": source_node_ids}
    return RecallQuery(
        query_id="query-001",
        query_text="task",
        requested_at="2026-06-14T10:01:00Z",
        filters=filters,
    )


def test_filter_events_by_query_source_nodes_matches_single_source() -> None:
    match = _event("event-001", "node-a")
    miss = _event("event-002", "node-b")

    assert filter_events_by_query_source_nodes((match, miss), _query("node-a")) == (
        match,
    )


def test_filter_events_by_query_source_nodes_matches_multiple_sources() -> None:
    first = _event("event-001", "node-a")
    second = _event("event-002", "node-b")
    third = _event("event-003", None)

    result = filter_events_by_query_source_nodes(
        (first, second, third),
        _query(("node-a", "node-b")),
    )

    assert result == (first, second)


def test_filter_events_by_query_source_nodes_noops_without_filter() -> None:
    event = _event("event-001", "node-a")

    assert filter_events_by_query_source_nodes((event,), _query()) == (event,)
