from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallQuery,
    TaskTrace,
)
from memory_aware_ros2_agent.recall_engine import TaskBasedRecallEngine


def _event(event_id: str, trace_id: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def _query(text: str, limit: int = 5) -> RecallQuery:
    return RecallQuery(
        query_id="query-001",
        query_text=text,
        requested_at="2026-06-14T10:01:00Z",
        limit=limit,
    )


def test_task_based_recall_returns_events_from_matching_trace() -> None:
    store = InMemoryStore()
    trace = TaskTrace("trace-001", "dock inspection", "2026-06-14T10:00:00Z")
    match = _event("event-001", "trace-001")
    miss = _event("event-002", "trace-002")
    store.save_trace(trace)
    store.save_trace(TaskTrace("trace-002", "charging", "2026-06-14T10:00:00Z"))
    store.save_event(match)
    store.save_event(miss)

    result = TaskBasedRecallEngine().recall(_query("dock"), store)

    assert result.events == (match,)
    assert result.scores == (1.0,)


def test_task_based_recall_returns_empty_for_no_task_match() -> None:
    store = InMemoryStore()
    store.save_trace(TaskTrace("trace-001", "charging", "2026-06-14T10:00:00Z"))
    store.save_event(_event("event-001", "trace-001"))

    result = TaskBasedRecallEngine().recall(_query("inspection"), store)

    assert result.events == ()


def test_task_based_recall_applies_query_limit() -> None:
    store = InMemoryStore()
    store.save_trace(TaskTrace("trace-001", "inspection", "2026-06-14T10:00:00Z"))
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-001")
    store.save_event(first)
    store.save_event(second)

    result = TaskBasedRecallEngine().recall(_query("inspection", limit=1), store)

    assert result.events == (first,)
