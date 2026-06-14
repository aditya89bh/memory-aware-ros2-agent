import json

from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.ros_compat import String
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_trace_subscriber_records_valid_trace_message() -> None:
    node = TraceSubscriber()
    message = String(
        data=json.dumps(
            {
                "trace_id": "trace-001",
                "task_name": "pick-and-place",
                "started_at": "2026-06-13T05:00:00Z",
                "events": [
                    {
                        "event_id": "event-001",
                        "trace_id": "trace-001",
                        "event_type": "task.started",
                        "timestamp": "2026-06-13T05:00:00Z",
                        "summary": "Robot started task.",
                        "payload": {},
                    }
                ],
                "ended_at": None,
            }
        )
    )

    node.record_trace(message)

    assert node.last_trace is not None
    assert node.last_trace.trace_id == "trace-001"
    assert node.last_trace.task_name == "pick-and-place"
    assert node.last_trace.events[0].event_type == EventType.TASK_STARTED


def test_trace_subscriber_ignores_invalid_trace_message() -> None:
    node = TraceSubscriber()

    node.record_trace(String(data="{not-json"))

    assert node.last_trace is None
