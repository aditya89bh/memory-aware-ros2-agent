from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallQuery,
    RecallResult,
)
from memory_aware_ros2_agent.recall_engine import RecallEngine


class StubRecallEngine:
    def recall(self, query: RecallQuery, store: InMemoryStore) -> RecallResult:
        return RecallResult(query_id=query.query_id, events=store.list_events())


def test_recall_engine_protocol_returns_result_from_store() -> None:
    store = InMemoryStore()
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Robot started inspection.",
    )
    store.save_event(event)
    query = RecallQuery(
        query_id="query-001",
        query_text="inspection started",
        requested_at="2026-06-14T10:01:00Z",
    )
    engine: RecallEngine = StubRecallEngine()

    result = engine.recall(query, store)

    assert result == RecallResult(query_id="query-001", events=(event,))
