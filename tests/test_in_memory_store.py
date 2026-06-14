from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallResult,
    TaskTrace,
)
from memory_aware_ros2_agent.persistence import MemoryStore


def _event(event_id: str, trace_id: str = "trace-001") -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )


def test_in_memory_store_saves_and_gets_events() -> None:
    store: MemoryStore = InMemoryStore()
    event = _event("event-001")

    store.save_event(event)

    assert store.get_event("event-001") == event
    assert store.list_events() == (event,)


def test_in_memory_store_filters_events_by_trace_id() -> None:
    store = InMemoryStore()
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-002")

    store.save_event(first)
    store.save_event(second)

    assert store.list_events("trace-001") == (first,)


def test_in_memory_store_replaces_events_by_id() -> None:
    store = InMemoryStore()
    original = _event("event-001")
    replacement = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:01:00Z",
        summary="Task observed.",
    )

    store.save_event(original)
    store.save_event(replacement)

    assert store.get_event("event-001") == replacement
    assert store.list_events() == (replacement,)


def test_in_memory_store_saves_and_gets_traces() -> None:
    store = InMemoryStore()
    event = _event("event-001")
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="inspect",
        started_at="2026-06-14T10:00:00Z",
        events=(event,),
    )

    store.save_trace(trace)

    assert store.get_trace("trace-001") == trace
    assert store.list_traces() == (trace,)


def test_in_memory_store_saves_and_gets_recall_results() -> None:
    store = InMemoryStore()
    result = RecallResult(query_id="query-001", generated_at="2026-06-14T10:00:00Z")

    store.save_recall_result(result)

    assert store.get_recall_result("query-001") == result
    assert store.list_recall_results() == (result,)
