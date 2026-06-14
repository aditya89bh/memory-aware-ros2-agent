import pytest

from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallQuery
from memory_aware_ros2_agent.recall_engine import (
    ExactMatchRecallEngine,
    composite_scores,
    event_types_from_query,
    paginate_events,
    rank_events_by_score,
)


def _query(**filters: object) -> RecallQuery:
    return RecallQuery(
        query_id="query-001",
        query_text="missing",
        requested_at="2026-06-14T10:00:00Z",
        filters=filters,
    )


def _event() -> MemoryEvent:
    return MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task event.",
    )


def test_exact_match_recall_handles_empty_store() -> None:
    result = ExactMatchRecallEngine().recall(_query(), InMemoryStore())

    assert result.events == ()
    assert result.scores == ()


def test_event_types_from_query_rejects_unknown_event_type() -> None:
    with pytest.raises(ValueError):
        event_types_from_query(_query(event_types=("unknown",)))


def test_rank_events_by_score_rejects_mismatched_scores() -> None:
    with pytest.raises(ValueError, match="same length"):
        rank_events_by_score((_event(),), ())


def test_composite_scores_rejects_empty_weight_sum() -> None:
    with pytest.raises(ValueError, match="positive"):
        composite_scores(((1.0,),), (0.0,))


def test_paginate_events_handles_offset_beyond_events() -> None:
    assert paginate_events((_event(),), _query(offset=10)) == ()
