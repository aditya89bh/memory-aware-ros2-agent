from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import (
    filter_events_by_query_event_types,
    filter_events_by_query_metadata,
    filter_events_by_query_source_nodes,
    filter_events_by_query_time_window,
)


def _event(
    event_id: str,
    event_type: EventType,
    timestamp: str,
    payload: dict[str, object],
) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary="Task event.",
        payload=payload,
    )


def test_combined_filters_narrow_events_incrementally() -> None:
    match = _event(
        "event-001",
        EventType.TASK_FAILED,
        "2026-06-14T10:01:00Z",
        {"zone": "dock", "source_node_id": "node-a"},
    )
    wrong_type = _event(
        "event-002",
        EventType.TASK_STARTED,
        "2026-06-14T10:01:00Z",
        {"zone": "dock", "source_node_id": "node-a"},
    )
    wrong_metadata = _event(
        "event-003",
        EventType.TASK_FAILED,
        "2026-06-14T10:01:00Z",
        {"zone": "lab", "source_node_id": "node-a"},
    )
    query = RecallQuery(
        query_id="query-001",
        query_text="dock",
        requested_at="2026-06-14T10:02:00Z",
        filters={
            "event_types": ("task.failed",),
            "started_at": "2026-06-14T10:00:00Z",
            "ended_at": "2026-06-14T10:02:00Z",
            "metadata": {"zone": "dock"},
            "source_node_ids": ("node-a",),
        },
    )
    events = (match, wrong_type, wrong_metadata)

    events = filter_events_by_query_event_types(events, query)
    events = filter_events_by_query_time_window(events, query)
    events = filter_events_by_query_metadata(events, query)
    events = filter_events_by_query_source_nodes(events, query)

    assert events == (match,)
