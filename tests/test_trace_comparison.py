from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import TraceComparison, compare_traces


def _event(
    trace_id: str, event_id: str, event_type: EventType, timestamp: str
) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_compare_traces_returns_aggregate_deltas() -> None:
    left = TaskTrace(
        "trace-left",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event(
                "trace-left",
                "event-1",
                EventType.TASK_SUCCEEDED,
                "2026-06-14T10:00:10Z",
            ),
        ),
        ended_at="2026-06-14T10:00:10Z",
    )
    right = TaskTrace(
        "trace-right",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event(
                "trace-right",
                "event-1",
                EventType.TASK_STARTED,
                "2026-06-14T10:00:01Z",
            ),
            _event(
                "trace-right",
                "event-2",
                EventType.TASK_FAILED,
                "2026-06-14T10:00:15Z",
            ),
        ),
        ended_at="2026-06-14T10:00:15Z",
    )

    assert compare_traces(left, right) == TraceComparison(
        left_trace_id="trace-left",
        right_trace_id="trace-right",
        duration_delta_seconds=5.0,
        event_count_delta=1,
        status_changed=True,
    )


def test_compare_traces_handles_missing_duration() -> None:
    left = TaskTrace("trace-left", "dock", "2026-06-14T10:00:00Z")
    right = TaskTrace("trace-right", "dock", "2026-06-14T10:00:00Z")

    assert compare_traces(left, right).duration_delta_seconds is None
