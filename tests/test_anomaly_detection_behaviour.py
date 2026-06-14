from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import detect_trace_anomalies


def _event(event_id: str, event_type: EventType, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_anomaly_detection_can_skip_terminal_event_requirement() -> None:
    trace = TaskTrace(
        "trace-001",
        "inspect",
        "2026-06-14T10:00:00Z",
        events=(_event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),),
    )

    assert detect_trace_anomalies(trace, require_terminal_event=False) == ()


def test_anomaly_detection_reports_multiple_anomalies() -> None:
    trace = TaskTrace(
        "trace-001",
        "inspect",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_FAILED, "2026-06-14T10:05:00Z"),
        ),
        ended_at="2026-06-14T10:05:00Z",
    )

    anomalies = detect_trace_anomalies(trace, max_duration_seconds=60.0)

    assert tuple(anomaly.anomaly_type for anomaly in anomalies) == (
        "duration_exceeded",
        "failure_after_success",
    )


def test_anomaly_detection_returns_no_anomalies_for_clean_trace() -> None:
    trace = TaskTrace(
        "trace-001",
        "inspect",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:02Z"),
        ),
        ended_at="2026-06-14T10:00:02Z",
    )

    assert detect_trace_anomalies(trace, max_duration_seconds=60.0) == ()
