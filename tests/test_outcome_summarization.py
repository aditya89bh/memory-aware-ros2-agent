from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    OutcomeSummary,
    OutcomeSummaryAnalyzer,
    summarize_outcome,
)


def _event(
    event_id: str,
    event_type: EventType,
    timestamp: str,
    reason: str | None = None,
) -> MemoryEvent:
    payload = {} if reason is None else {"reason": reason}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_type.value} summary",
        payload=payload,
    )


def test_summarize_outcome_returns_latest_terminal_event() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:02Z"),
        ),
        ended_at="2026-06-14T10:00:02Z",
    )

    assert summarize_outcome(trace) == OutcomeSummary(
        status="succeeded",
        reason="task.succeeded summary",
        duration_seconds=2.0,
        terminal_event_id="event-2",
    )


def test_summarize_outcome_prefers_payload_reason() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "2026-06-14T10:00:01Z", "timeout"),
        ),
    )

    assert summarize_outcome(trace).reason == "timeout"


def test_summarize_outcome_handles_missing_terminal_event() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    assert summarize_outcome(trace) == OutcomeSummary("unknown", None, None, None)


def test_outcome_summary_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = OutcomeSummaryAnalyzer().analyze(trace)

    assert insight.insight_type == "outcome_summary"
    assert insight.details["status"] == "unknown"
