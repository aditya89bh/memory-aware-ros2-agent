from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    SuccessPatternAnalyzer,
    success_events,
    success_pattern_counts,
)


def _event(
    event_id: str,
    event_type: EventType,
    summary: str,
    signal: str | None = None,
) -> MemoryEvent:
    payload = {} if signal is None else {"signal": signal}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp="2026-06-14T10:00:00Z",
        summary=summary,
        payload=payload,
    )


def test_success_events_returns_only_success_events() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_OBSERVED, "Saw dock."),
            _event("event-2", EventType.TASK_SUCCEEDED, "Docked."),
        ),
    )

    assert tuple(event.event_id for event in success_events(trace)) == ("event-2",)


def test_success_pattern_counts_prefers_payload_signal() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_SUCCEEDED, "Docked.", "aligned"),
            _event("event-2", EventType.TASK_SUCCEEDED, "Docked.", "aligned"),
            _event("event-3", EventType.TASK_SUCCEEDED, "Battery charging."),
        ),
    )

    assert success_pattern_counts(trace) == {"Battery charging.": 1, "aligned": 2}


def test_success_pattern_analyzer_summarizes_dominant_signal() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_SUCCEEDED, "Docked.", "aligned"),
            _event("event-2", EventType.TASK_SUCCEEDED, "Docked.", "aligned"),
        ),
    )

    insight = SuccessPatternAnalyzer().analyze(trace)

    assert insight.insight_type == "success_patterns"
    assert insight.details["success_count"] == 2
    assert "aligned" in insight.summary


def test_success_pattern_analyzer_handles_trace_without_successes() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = SuccessPatternAnalyzer().analyze(trace)

    assert insight.details == {"success_count": 0, "patterns": {}}
