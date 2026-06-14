from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    EventSequenceAnalyzer,
    extract_event_sequence,
)


def _event(event_id: str, event_type: EventType, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_extract_event_sequence_orders_events_by_timestamp() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-2", EventType.TASK_ACTED, "2026-06-14T10:00:02Z"),
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
        ),
    )

    sequence = extract_event_sequence(trace)

    assert tuple(step.event_id for step in sequence) == ("event-1", "event-2")
    assert tuple(step.index for step in sequence) == (1, 0)


def test_extract_event_sequence_preserves_original_order_for_ties() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_ACTED, "2026-06-14T10:00:01Z"),
        ),
    )

    sequence = extract_event_sequence(trace)

    assert tuple(step.event_id for step in sequence) == ("event-1", "event-2")


def test_event_sequence_analyzer_returns_serializable_steps() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(_event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),),
    )

    insight = EventSequenceAnalyzer().analyze(trace)

    assert insight.insight_type == "event_sequence"
    assert insight.details["sequence"] == (
        {
            "index": 0,
            "event_id": "event-1",
            "event_type": "task.started",
            "timestamp": "2026-06-14T10:00:01Z",
            "summary": "event-1 summary",
        },
    )
