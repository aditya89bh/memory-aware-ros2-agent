"""ROS2 node for subscribing to serialized task traces."""

from __future__ import annotations

import json

from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.ros_compat import Node, String
from memory_aware_ros2_agent.serialization import task_trace_from_dict


class TraceSubscriber(Node):
    """Subscribe to task trace JSON messages and keep the latest trace in memory."""

    def __init__(self) -> None:
        super().__init__("trace_subscriber")
        self.last_trace: TaskTrace | None = None
        self.create_subscription(String, "memory/traces", self.record_trace, 10)

    def record_trace(self, message: String) -> None:
        """Record one incoming task trace message."""

        try:
            payload = json.loads(message.data)
            self.last_trace = task_trace_from_dict(payload)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self.get_logger().error(f"Failed to record task trace: {exc}")
            return

        self.get_logger().info(f"Recorded task trace {self.last_trace.trace_id}")


def main() -> None:
    """Run the trace subscriber node."""

    from memory_aware_ros2_agent.ros_compat import rclpy

    if rclpy is None:
        raise RuntimeError("rclpy is required to run TraceSubscriber")

    rclpy.init()
    node = TraceSubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
