from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    ExecutionStatisticsAnalyzer,
    calculate_execution_statistics,
)


def _event(event_id: str, event_type: EventType, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_calculate_execution_statistics_counts_events_and_outcome() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_FAILED, "2026-06-14T10:00:02Z"),
            _event("event-3", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:03Z"),
        ),
        ended_at="2026-06-14T10:00:03Z",
    )

    statistics = calculate_execution_statistics(trace)

    assert statistics.event_count == 3
    assert statistics.duration_seconds == 3.0
    assert statistics.event_type_counts == {
        "task.failed": 1,
        "task.started": 1,
        "task.succeeded": 1,
    }
    assert statistics.failure_count == 1
    assert statistics.success_count == 1
    assert statistics.status == "succeeded"


def test_execution_statistics_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = ExecutionStatisticsAnalyzer().analyze(trace)

    assert insight.insight_type == "execution_statistics"
    assert insight.details["event_count"] == 0
    assert insight.details["status"] == "unknown"
