from memory_aware_ros2_agent.factories import create_memory_event
from memory_aware_ros2_agent.models import EventType


def test_create_memory_event_uses_generated_defaults() -> None:
    event = create_memory_event(
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        summary="Robot started task.",
    )

    assert event.event_id.startswith("event-")
    assert event.trace_id == "trace-001"
    assert event.event_type == EventType.TASK_STARTED
    assert event.timestamp.endswith("Z")
    assert event.payload == {}


def test_create_memory_event_accepts_explicit_values() -> None:
    event = create_memory_event(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_OBSERVED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot observed object.",
        payload={"object_id": "part-7"},
    )

    assert event.event_id == "event-001"
    assert event.timestamp == "2026-06-13T05:00:00Z"
    assert event.payload == {"object_id": "part-7"}
