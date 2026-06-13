"""ROS2 node for publishing serialized task traces."""

from __future__ import annotations

import json
from typing import Any

from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.ros_compat import Node, String
from memory_aware_ros2_agent.serialization import model_to_dict


class TracePublisher(Node):
    """Publish task traces as JSON strings."""

    def __init__(self) -> None:
        super().__init__("trace_publisher")
        self.publisher = self.create_publisher(String, "memory/traces", 10)

    def serialize_trace(self, trace: TaskTrace) -> String:
        """Serialize a task trace into a ROS string message."""

        return String(data=json.dumps(model_to_dict(trace), sort_keys=True))

    def publish_trace(self, trace: TaskTrace) -> None:
        """Publish one task trace."""

        message = self.serialize_trace(trace)
        publisher = self.publisher
        if publisher is not None:
            publisher.publish(message)
        self.get_logger().info(f"Published task trace {trace.trace_id}")


def main() -> None:
    """Run the trace publisher node."""

    from memory_aware_ros2_agent.ros_compat import rclpy

    if rclpy is None:
        raise RuntimeError("rclpy is required to run TracePublisher")

    rclpy.init()
    node = TracePublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


def publish_trace_for_test(node: TracePublisher, trace: TaskTrace) -> Any:
    """Publish a trace and return the serialized message for tests."""

    message = node.serialize_trace(trace)
    node.publish_trace(trace)
    return message
