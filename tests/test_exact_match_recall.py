from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


def _event(
    event_id: str,
    summary: str,
    trace_id: str = "trace-001",
    payload: dict[str, str] | None = None,
) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary=summary,
        payload={} if payload is None else payload,
    )


def _query(text: str, trace_id: str | None = None, limit: int = 5) -> RecallQuery:
    return RecallQuery(
        query_id="query-001",
        query_text=text,
        requested_at="2026-06-14T10:01:00Z",
        trace_id=trace_id,
        limit=limit,
    )


def test_exact_match_recall_matches_event_summary() -> None:
    store = InMemoryStore()
    match = _event("event-001", "Robot inspected the loading dock.")
    miss = _event("event-002", "Robot charged battery.")
    store.save_event(match)
    store.save_event(miss)

    result = ExactMatchRecallEngine().recall(_query("loading dock"), store)

    assert result.events == (match,)
    assert result.scores == (1.0,)


def test_exact_match_recall_matches_payload_text() -> None:
    store = InMemoryStore()
    event = _event("event-001", "Robot observed object.", payload={"zone": "dock"})
    store.save_event(event)

    result = ExactMatchRecallEngine().recall(_query("zone dock"), store)

    assert result.events == (event,)


def test_exact_match_recall_filters_trace_and_limit() -> None:
    store = InMemoryStore()
    first = _event("event-001", "Robot inspected dock.", "trace-001")
    second = _event("event-002", "Robot inspected dock.", "trace-002")
    store.save_event(first)
    store.save_event(second)

    result = ExactMatchRecallEngine().recall(
        _query("inspected", trace_id="trace-001", limit=1),
        store,
    )

    assert result.events == (first,)


def test_exact_match_recall_ignores_empty_query_text() -> None:
    store = InMemoryStore()
    store.save_event(_event("event-001", "Robot inspected dock."))

    result = ExactMatchRecallEngine().recall(_query("  "), store)

    assert result.events == ()
    assert result.scores == ()
