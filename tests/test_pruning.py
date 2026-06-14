from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallResult,
    TaskTrace,
)
from memory_aware_ros2_agent.pruning import PruneResult, prune_store
from memory_aware_ros2_agent.retention import RetentionPolicy


def _event(event_id: str, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary="Task event.",
    )


def test_prune_store_removes_oldest_records_by_policy() -> None:
    store = InMemoryStore()
    store.save_event(_event("event-001", "2026-06-14T10:00:00Z"))
    keep_event = _event("event-002", "2026-06-14T10:01:00Z")
    store.save_event(keep_event)
    store.save_trace(TaskTrace("trace-001", "inspect", "2026-06-14T10:00:00Z"))
    keep_trace = TaskTrace("trace-002", "inspect", "2026-06-14T10:01:00Z")
    store.save_trace(keep_trace)
    store.save_recall_result(
        RecallResult("query-001", generated_at="2026-06-14T10:00:00Z")
    )
    keep_result = RecallResult("query-002", generated_at="2026-06-14T10:01:00Z")
    store.save_recall_result(keep_result)

    result = prune_store(
        store,
        RetentionPolicy(max_events=1, max_traces=1, max_recall_results=1),
    )

    assert result == PruneResult(
        events_removed=1,
        traces_removed=1,
        recall_results_removed=1,
    )
    assert store.list_events() == (keep_event,)
    assert store.list_traces() == (keep_trace,)
    assert store.list_recall_results() == (keep_result,)


def test_prune_store_noops_for_unbounded_policy() -> None:
    store = InMemoryStore()
    event = _event("event-001", "2026-06-14T10:00:00Z")
    store.save_event(event)

    result = prune_store(store, RetentionPolicy())

    assert result == PruneResult()
    assert store.list_events() == (event,)
