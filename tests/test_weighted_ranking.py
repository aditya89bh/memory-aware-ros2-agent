import pytest

from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.recall_engine import rank_events_by_score


def _event(event_id: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def test_rank_events_by_score_sorts_descending() -> None:
    first = _event("event-001")
    second = _event("event-002")
    third = _event("event-003")

    assert rank_events_by_score((first, second, third), (0.2, 1.0, 0.5)) == (
        second,
        third,
        first,
    )


def test_rank_events_by_score_preserves_stable_ties() -> None:
    first = _event("event-001")
    second = _event("event-002")

    assert rank_events_by_score((first, second), (1.0, 1.0)) == (first, second)


def test_rank_events_by_score_requires_score_for_each_event() -> None:
    with pytest.raises(ValueError, match="same length"):
        rank_events_by_score((_event("event-001"),), ())
