from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    FailurePatternAnalyzer,
    failure_events,
    failure_pattern_counts,
)


def _event(
    event_id: str,
    event_type: EventType,
    summary: str,
    reason: str | None = None,
) -> MemoryEvent:
    payload = {} if reason is None else {"reason": reason}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp="2026-06-14T10:00:00Z",
        summary=summary,
        payload=payload,
    )


def test_failure_events_returns_only_failed_events() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_OBSERVED, "Saw dock."),
            _event("event-2", EventType.TASK_FAILED, "Docking failed."),
        ),
    )

    assert tuple(event.event_id for event in failure_events(trace)) == ("event-2",)


def test_failure_pattern_counts_prefers_payload_reason() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "Failed.", "timeout"),
            _event("event-2", EventType.TASK_FAILED, "Failed.", "timeout"),
            _event("event-3", EventType.TASK_FAILED, "Obstacle blocked path."),
        ),
    )

    assert failure_pattern_counts(trace) == {
        "Obstacle blocked path.": 1,
        "timeout": 2,
    }


def test_failure_pattern_analyzer_summarizes_dominant_failure() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "Failed.", "timeout"),
            _event("event-2", EventType.TASK_FAILED, "Failed.", "timeout"),
        ),
    )

    insight = FailurePatternAnalyzer().analyze(trace)

    assert insight.insight_type == "failure_patterns"
    assert insight.details["failure_count"] == 2
    assert "timeout" in insight.summary


def test_failure_pattern_analyzer_handles_successful_trace() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = FailurePatternAnalyzer().analyze(trace)

    assert insight.details == {"failure_count": 0, "patterns": {}}
