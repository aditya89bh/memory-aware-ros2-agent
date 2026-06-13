import json

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.ros_compat import String


def test_memory_recorder_records_valid_event_message() -> None:
    node = MemoryRecorder()
    message = String(
        data=json.dumps(
            {
                "event_id": "event-001",
                "trace_id": "trace-001",
                "event_type": "task.started",
                "timestamp": "2026-06-13T05:00:00Z",
                "summary": "Robot started task.",
                "payload": {},
            }
        )
    )

    node.record_event(message)

    assert node.last_event is not None
    assert node.last_event.event_id == "event-001"
    assert node.last_event.event_type == EventType.TASK_STARTED


def test_memory_recorder_ignores_invalid_event_message() -> None:
    node = MemoryRecorder()

    node.record_event(String(data="{not-json"))

    assert node.last_event is None
