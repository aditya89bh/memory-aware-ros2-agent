"""ROS2 node for recording memory events from JSON messages."""

from __future__ import annotations

import json

from memory_aware_ros2_agent.models import MemoryEvent
from memory_aware_ros2_agent.ros_compat import Node, String
from memory_aware_ros2_agent.serialization import memory_event_from_dict


class MemoryRecorder(Node):
    """Subscribe to memory event JSON messages and keep the latest event in memory."""

    def __init__(self) -> None:
        super().__init__("memory_recorder")
        self.last_event: MemoryEvent | None = None
        self.create_subscription(String, "memory/events", self.record_event, 10)

    def record_event(self, message: String) -> None:
        """Record one incoming memory event message."""

        try:
            payload = json.loads(message.data)
            self.last_event = memory_event_from_dict(payload)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self.get_logger().error(f"Failed to record memory event: {exc}")
            return

        self.get_logger().info(f"Recorded memory event {self.last_event.event_id}")


def main() -> None:
    """Run the memory recorder node."""

    from memory_aware_ros2_agent.ros_compat import rclpy

    if rclpy is None:
        raise RuntimeError("rclpy is required to run MemoryRecorder")

    rclpy.init()
    node = MemoryRecorder()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
