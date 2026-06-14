from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    ExperienceSummaryAnalyzer,
    summarize_experience,
)


def _event(
    event_id: str, event_type: EventType, reason: str | None = None
) -> MemoryEvent:
    payload = {} if reason is None else {"reason": reason}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=f"2026-06-14T10:00:0{event_id[-1]}Z",
        summary=f"{event_id} summary",
        payload=payload,
    )


def test_summarize_experience_builds_high_level_highlights() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "timeout"),
            _event("event-2", EventType.TASK_FAILED, "timeout"),
        ),
        ended_at="2026-06-14T10:00:02Z",
    )

    summary = summarize_experience(trace)

    assert summary.trace_id == "trace-001"
    assert summary.task_name == "dock"
    assert summary.status == "failed"
    assert "Task dock failed." in summary.highlights
    assert "Recorded 2 events." in summary.highlights
    assert "Repeated failure: timeout (2 times)." in summary.highlights


def test_experience_summary_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = ExperienceSummaryAnalyzer().analyze(trace)

    assert insight.insight_type == "experience_summary"
    assert insight.details["task_name"] == "dock"
    assert insight.details["status"] == "unknown"
