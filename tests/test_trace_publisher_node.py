import json

from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.trace_publisher_node import (
    TracePublisher,
    publish_trace_for_test,
)


def test_trace_publisher_serializes_task_trace() -> None:
    node = TracePublisher()
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
    )

    message = node.serialize_trace(trace)
    payload = json.loads(message.data)

    assert payload["trace_id"] == "trace-001"
    assert payload["task_name"] == "pick-and-place"
    assert payload["events"] == []


def test_publish_trace_for_test_returns_serialized_message() -> None:
    node = TracePublisher()
    trace = TaskTrace(
        trace_id="trace-002",
        task_name="dock",
        started_at="2026-06-13T05:30:00Z",
    )

    message = publish_trace_for_test(node, trace)

    assert json.loads(message.data)["trace_id"] == "trace-002"
