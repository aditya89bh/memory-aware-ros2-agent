from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery


def test_memory_events_compare_by_value() -> None:
    first = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
        payload={"attempt": 1},
    )
    second = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
        payload={"attempt": 1},
    )

    assert first == second


def test_memory_events_are_hashable_with_payloads() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
        payload={"attempt": 1},
    )

    assert event in {event}


def test_recall_queries_are_hashable_with_filters() -> None:
    query = RecallQuery(
        query_id="query-001",
        query_text="Find failures.",
        requested_at="2026-06-13T05:10:00Z",
        filters={"event_type": "task.failed"},
    )

    assert query in {query}
