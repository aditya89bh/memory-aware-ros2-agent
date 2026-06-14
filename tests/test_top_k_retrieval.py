from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.recall_engine import top_k_events


def _event(event_id: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def test_top_k_events_returns_highest_scored_events() -> None:
    first = _event("event-001")
    second = _event("event-002")
    third = _event("event-003")

    assert top_k_events((first, second, third), (0.2, 1.0, 0.5), 2) == (
        second,
        third,
    )


def test_top_k_events_returns_empty_for_non_positive_k() -> None:
    assert top_k_events((_event("event-001"),), (1.0,), 0) == ()


def test_top_k_events_allows_k_larger_than_event_count() -> None:
    event = _event("event-001")

    assert top_k_events((event,), (1.0,), 5) == (event,)
