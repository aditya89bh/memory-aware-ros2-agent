import pytest

from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallResult
from memory_aware_ros2_agent.recall_engine import (
    RecallExplanation,
    explain_recall_result,
)


def _event() -> MemoryEvent:
    return MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_FAILED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Robot failed to dock.",
    )


def test_explain_recall_result_uses_scores_and_event_context() -> None:
    event = _event()
    result = RecallResult(query_id="query-001", events=(event,), scores=(0.75,))

    assert explain_recall_result(result) == (
        RecallExplanation(
            event_id="event-001",
            score=0.75,
            reason="Matched task.failed event: Robot failed to dock.",
        ),
    )


def test_explain_recall_result_defaults_scores() -> None:
    event = _event()

    explanations = explain_recall_result(
        RecallResult(query_id="query-001", events=(event,))
    )

    assert explanations[0].score == 1.0


def test_explain_recall_result_requires_score_alignment() -> None:
    with pytest.raises(ValueError, match="scores"):
        explain_recall_result(
            RecallResult(query_id="query-001", events=(_event(),), scores=(0.1, 0.2))
        )
