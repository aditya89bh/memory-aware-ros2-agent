from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
    task_trace_from_dict,
)


def test_memory_event_from_dict_round_trips_serialized_event() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )

    assert memory_event_from_dict(model_to_dict(event)) == event


def test_task_trace_from_dict_round_trips_nested_events() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
        events=(event,),
    )

    assert task_trace_from_dict(model_to_dict(trace)) == trace
