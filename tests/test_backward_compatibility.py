from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    task_trace_from_dict,
)


def test_memory_event_deserializes_payload_missing_from_older_payloads() -> None:
    payload = {
        "event_id": "event-001",
        "trace_id": "trace-001",
        "event_type": "task.started",
        "timestamp": "2026-06-13T05:00:00Z",
        "summary": "Robot started task.",
    }

    assert memory_event_from_dict(payload) == MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )


def test_task_trace_deserializes_ended_at_missing_from_older_payloads() -> None:
    payload = {
        "trace_id": "trace-001",
        "task_name": "pick-and-place",
        "started_at": "2026-06-13T05:00:00Z",
        "events": [],
    }

    assert task_trace_from_dict(payload) == TaskTrace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
    )
