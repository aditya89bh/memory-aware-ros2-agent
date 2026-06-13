from memory_aware_ros2_agent.models import MemoryEvent


def test_memory_event_stores_required_fields() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type="task.started",
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started pick workflow.",
    )

    assert event.event_id == "event-001"
    assert event.trace_id == "trace-001"
    assert event.event_type == "task.started"
    assert event.timestamp == "2026-06-13T05:00:00Z"
    assert event.summary == "Robot started pick workflow."
    assert event.payload == {}


def test_memory_event_accepts_payload() -> None:
    event = MemoryEvent(
        event_id="event-002",
        trace_id="trace-001",
        event_type="task.observed",
        timestamp="2026-06-13T05:01:00Z",
        summary="Robot observed object pose.",
        payload={"object_id": "part-7", "confidence": 0.92},
    )

    assert event.payload == {"object_id": "part-7", "confidence": 0.92}
