from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.recall_engine import recency_scores


def _event(event_id: str, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary="Task event.",
    )


def test_recency_scores_empty_events() -> None:
    assert recency_scores(()) == ()


def test_recency_scores_single_event_as_most_recent() -> None:
    assert recency_scores((_event("event-001", "2026-06-14T10:00:00Z"),)) == (1.0,)


def test_recency_scores_rank_newer_timestamps_higher() -> None:
    old = _event("event-001", "2026-06-14T10:00:00Z")
    new = _event("event-002", "2026-06-14T10:02:00Z")
    middle = _event("event-003", "2026-06-14T10:01:00Z")

    assert recency_scores((old, new, middle)) == (0.0, 1.0, 0.5)


def test_recency_scores_tied_timestamps_share_score() -> None:
    first = _event("event-001", "2026-06-14T10:00:00Z")
    second = _event("event-002", "2026-06-14T10:00:00Z")

    assert recency_scores((first, second)) == (1.0, 1.0)
