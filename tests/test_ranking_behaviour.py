from memory_aware_ros2_agent.models import EventType, MemoryEvent
from memory_aware_ros2_agent.recall_engine import (
    composite_scores,
    frequency_scores,
    recency_scores,
    top_k_events,
)


def _event(event_id: str, trace_id: str, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary="Task event.",
    )


def test_ranking_combines_recency_and_frequency_for_top_k() -> None:
    repeated_old = _event("event-001", "trace-a", "2026-06-14T10:00:00Z")
    repeated_new = _event("event-002", "trace-a", "2026-06-14T10:01:00Z")
    single_newest = _event("event-003", "trace-b", "2026-06-14T10:02:00Z")
    events = (repeated_old, repeated_new, single_newest)

    scores = composite_scores(
        (recency_scores(events), frequency_scores(events)),
        (1.0, 1.0),
    )

    assert top_k_events(events, scores, 2) == (repeated_new, single_newest)


def test_ranking_prefers_newest_when_recency_weight_dominates() -> None:
    older = _event("event-001", "trace-a", "2026-06-14T10:00:00Z")
    newer = _event("event-002", "trace-b", "2026-06-14T10:01:00Z")
    events = (older, newer)

    scores = composite_scores(
        (recency_scores(events), frequency_scores(events)),
        (5.0, 1.0),
    )

    assert top_k_events(events, scores, 1) == (newer,)
