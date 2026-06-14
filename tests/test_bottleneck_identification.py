from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    BottleneckAnalyzer,
    TraceBottleneck,
    identify_bottlenecks,
)


def _event(event_id: str, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_identify_bottlenecks_returns_gaps_above_threshold() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", "2026-06-14T10:00:01Z"),
            _event("event-2", "2026-06-14T10:00:31Z"),
            _event("event-3", "2026-06-14T10:00:35Z"),
        ),
    )

    assert identify_bottlenecks(trace, minimum_gap_seconds=10.0) == (
        TraceBottleneck("event-1", "event-2", 30.0),
    )


def test_identify_bottlenecks_handles_short_traces() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    assert identify_bottlenecks(trace, minimum_gap_seconds=10.0) == ()


def test_bottleneck_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", "2026-06-14T10:00:01Z"),
            _event("event-2", "2026-06-14T10:00:21Z"),
        ),
    )

    insight = BottleneckAnalyzer(minimum_gap_seconds=5.0).analyze(trace)

    assert insight.insight_type == "bottlenecks"
    assert insight.details["bottlenecks"] == (
        {
            "from_event_id": "event-1",
            "to_event_id": "event-2",
            "duration_seconds": 20.0,
        },
    )
