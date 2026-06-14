from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    StateTransition,
    StateTransitionAnalyzer,
    analyze_state_transitions,
)


def _event(event_id: str, event_type: EventType, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_analyze_state_transitions_counts_adjacent_event_types() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_ACTED, "2026-06-14T10:00:02Z"),
            _event("event-3", EventType.TASK_FAILED, "2026-06-14T10:00:03Z"),
            _event("event-4", EventType.TASK_ACTED, "2026-06-14T10:00:04Z"),
            _event("event-5", EventType.TASK_FAILED, "2026-06-14T10:00:05Z"),
        ),
    )

    assert analyze_state_transitions(trace) == (
        StateTransition(EventType.TASK_ACTED, EventType.TASK_FAILED, 2),
        StateTransition(EventType.TASK_FAILED, EventType.TASK_ACTED, 1),
        StateTransition(EventType.TASK_STARTED, EventType.TASK_ACTED, 1),
    )


def test_analyze_state_transitions_handles_single_event_trace() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(_event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),),
    )

    assert analyze_state_transitions(trace) == ()


def test_state_transition_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:02Z"),
        ),
    )

    insight = StateTransitionAnalyzer().analyze(trace)

    assert insight.insight_type == "state_transitions"
    assert insight.details["transitions"] == (
        {
            "from_event_type": "task.started",
            "to_event_type": "task.succeeded",
            "count": 1,
        },
    )
