from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    RepeatedFailure,
    RepeatedFailureAnalyzer,
    detect_repeated_failures,
)


def _failure(event_id: str, reason: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_FAILED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task failed.",
        payload={"reason": reason},
    )


def test_detect_repeated_failures_returns_reasons_above_threshold() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _failure("event-1", "timeout"),
            _failure("event-2", "timeout"),
            _failure("event-3", "blocked"),
        ),
    )

    assert detect_repeated_failures(trace) == (RepeatedFailure("timeout", 2),)


def test_detect_repeated_failures_respects_custom_threshold() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _failure("event-1", "timeout"),
            _failure("event-2", "timeout"),
        ),
    )

    assert detect_repeated_failures(trace, minimum_count=3) == ()


def test_repeated_failure_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _failure("event-1", "timeout"),
            _failure("event-2", "timeout"),
        ),
    )

    insight = RepeatedFailureAnalyzer().analyze(trace)

    assert insight.insight_type == "repeated_failures"
    assert insight.details["repeated_failures"] == (
        {"reason": "timeout", "count": 2},
    )
