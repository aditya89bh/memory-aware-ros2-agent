from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import build_replay_steps


def _event(event_id: str, timestamp: str, summary: str | None = None) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp=timestamp,
        summary=summary or f"{event_id} summary",
    )


def test_replay_steps_keep_zero_delay_for_equal_timestamps() -> None:
    trace = TaskTrace(
        "trace-001",
        "inspect",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", "2026-06-14T10:00:01Z"),
            _event("event-2", "2026-06-14T10:00:01Z"),
        ),
    )

    steps = build_replay_steps(trace)

    assert tuple(step.delay_since_previous_seconds for step in steps) == (0.0, 0.0)


def test_replay_steps_preserve_event_summaries() -> None:
    trace = TaskTrace(
        "trace-001",
        "inspect",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", "2026-06-14T10:00:01Z", "Observed aisle."),
        ),
    )

    steps = build_replay_steps(trace)

    assert steps[0].summary == "Observed aisle."
