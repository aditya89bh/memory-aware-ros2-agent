from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.models import EventType


def test_create_task_trace_uses_generated_defaults() -> None:
    trace = create_task_trace(task_name="pick-and-place")

    assert trace.trace_id.startswith("trace-")
    assert trace.task_name == "pick-and-place"
    assert trace.started_at.endswith("Z")
    assert trace.events == ()
    assert trace.ended_at is None


def test_create_task_trace_accepts_events_and_explicit_values() -> None:
    event = create_memory_event(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )
    trace = create_task_trace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
        events=(event,),
        ended_at="2026-06-13T05:10:00Z",
    )

    assert trace.events == (event,)
    assert trace.ended_at == "2026-06-13T05:10:00Z"
