from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    analyze_state_transitions,
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


def test_sequence_analysis_supports_transition_pipeline() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-3", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:03Z"),
            _event("event-1", EventType.TASK_STARTED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_ACTED, "2026-06-14T10:00:02Z"),
        ),
    )

    sequence = extract_event_sequence(trace)
    transitions = analyze_state_transitions(trace)

    assert tuple(step.event_type for step in sequence) == (
        EventType.TASK_STARTED,
        EventType.TASK_ACTED,
        EventType.TASK_SUCCEEDED,
    )
    assert tuple(
        (transition.from_event_type, transition.to_event_type)
        for transition in transitions
    ) == (
        (EventType.TASK_ACTED, EventType.TASK_SUCCEEDED),
        (EventType.TASK_STARTED, EventType.TASK_ACTED),
    )


def test_sequence_analysis_handles_duplicate_event_types() -> None:
    trace = TaskTrace(
        "trace-001",
        "observe",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_OBSERVED, "2026-06-14T10:00:01Z"),
            _event("event-2", EventType.TASK_OBSERVED, "2026-06-14T10:00:02Z"),
            _event("event-3", EventType.TASK_OBSERVED, "2026-06-14T10:00:03Z"),
        ),
    )

    transitions = analyze_state_transitions(trace)

    assert transitions[0].count == 2
