from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.recall_engine import frequency_scores


def _event(event_id: str, trace_id: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def test_frequency_scores_empty_events() -> None:
    assert frequency_scores(()) == ()


def test_frequency_scores_equal_frequency_as_full_score() -> None:
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-002")

    assert frequency_scores((first, second)) == (1.0, 1.0)


def test_frequency_scores_boosts_more_frequent_trace() -> None:
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-001")
    third = _event("event-003", "trace-002")

    assert frequency_scores((first, second, third)) == (1.0, 1.0, 0.5)
