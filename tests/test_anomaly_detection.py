from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    TraceAnomalyAnalyzer,
    detect_trace_anomalies,
)


def _event(event_id: str, event_type: EventType, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_type.value} event",
    )


def test_detect_trace_anomalies_reports_missing_terminal_event() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(_event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),),
    )

    anomalies = detect_trace_anomalies(trace)

    assert tuple(anomaly.anomaly_type for anomaly in anomalies) == (
        "missing_terminal_event",
    )


def test_detect_trace_anomalies_reports_excessive_duration() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_SUCCEEDED, "2026-06-14T10:05:00Z"),
        ),
        ended_at="2026-06-14T10:05:00Z",
    )

    anomalies = detect_trace_anomalies(trace, max_duration_seconds=60.0)

    assert tuple(anomaly.anomaly_type for anomaly in anomalies) == (
        "duration_exceeded",
    )


def test_detect_trace_anomalies_reports_failure_after_success() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_FAILED, "2026-06-14T10:00:02Z"),
        ),
    )

    anomalies = detect_trace_anomalies(trace)

    assert tuple(anomaly.anomaly_type for anomaly in anomalies) == (
        "failure_after_success",
    )


def test_trace_anomaly_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    insight = TraceAnomalyAnalyzer().analyze(trace)

    assert insight.insight_type == "trace_anomalies"
    assert insight.details["anomalies"][0]["anomaly_type"] == "missing_terminal_event"
