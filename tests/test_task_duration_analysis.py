from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    TaskDurationAnalyzer,
    task_duration_seconds,
)


def _event(timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=f"event-{timestamp}",
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary="Task event.",
    )


def test_task_duration_seconds_uses_trace_end_time() -> None:
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="dock",
        started_at="2026-06-14T10:00:00Z",
        ended_at="2026-06-14T10:02:30Z",
    )

    assert task_duration_seconds(trace) == 150.0


def test_task_duration_seconds_uses_latest_event_when_trace_is_open() -> None:
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="dock",
        started_at="2026-06-14T10:00:00Z",
        events=(
            _event("2026-06-14T10:01:00Z"),
            _event("2026-06-14T10:02:00Z"),
        ),
    )

    assert task_duration_seconds(trace) == 120.0


def test_task_duration_seconds_returns_none_without_end_or_events() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    assert task_duration_seconds(trace) is None


def test_task_duration_analyzer_returns_insight() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        ended_at="2026-06-14T10:00:05Z",
    )

    insight = TaskDurationAnalyzer().analyze(trace)

    assert insight.insight_type == "task_duration"
    assert insight.details["duration_seconds"] == 5.0
