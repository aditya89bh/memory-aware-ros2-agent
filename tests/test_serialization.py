from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.serialization import model_to_dict


def test_model_to_dict_serializes_memory_event() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )

    assert model_to_dict(event) == {
        "event_id": "event-001",
        "trace_id": "trace-001",
        "event_type": "task.started",
        "timestamp": "2026-06-13T05:00:00Z",
        "summary": "Robot started task.",
        "payload": {},
    }


def test_model_to_dict_serializes_nested_trace_events() -> None:
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

    serialized = model_to_dict(trace)

    assert serialized["events"] == [model_to_dict(event)]
