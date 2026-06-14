from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import ReplayStep, build_replay_steps


def _event(event_id: str, timestamp: str) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_ACTED,
        timestamp=timestamp,
        summary=f"{event_id} summary",
    )


def test_build_replay_steps_calculates_relative_delays() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-2", "2026-06-14T10:00:05Z"),
            _event("event-1", "2026-06-14T10:00:01Z"),
            _event("event-3", "2026-06-14T10:00:08Z"),
        ),
    )

    assert build_replay_steps(trace) == (
        ReplayStep("event-1", EventType.TASK_ACTED, 0.0, "event-1 summary"),
        ReplayStep("event-2", EventType.TASK_ACTED, 4.0, "event-2 summary"),
        ReplayStep("event-3", EventType.TASK_ACTED, 3.0, "event-3 summary"),
    )


def test_build_replay_steps_handles_empty_trace() -> None:
    trace = TaskTrace("trace-001", "dock", "2026-06-14T10:00:00Z")

    assert build_replay_steps(trace) == ()
