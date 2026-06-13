"""ROS2 node exposing a recall service interface."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.ros_compat import Node, Trigger


class RecallService(Node):
    """Expose a recall service placeholder without implementing recall algorithms."""

    def __init__(self) -> None:
        super().__init__("recall_service")
        self.create_service(Trigger, "memory/recall", self.handle_recall)

    def handle_recall(
        self,
        _request: Trigger.Request,
        response: Trigger.Response,
    ) -> Trigger.Response:
        """Return a clear placeholder response for future recall implementations."""

        response.success = False
        response.message = "Recall algorithms are not implemented yet."
        self.get_logger().info("Received recall request")
        return response


def main() -> None:
    """Run the recall service node."""

    from memory_aware_ros2_agent.ros_compat import rclpy

    if rclpy is None:
        raise RuntimeError("rclpy is required to run RecallService")

    rclpy.init()
    node = RecallService()
    try:
        rclpy.spin(node)
    finally:
        destroy_node = getattr(node, "destroy_node")
        destroy_node()
        rclpy.shutdown()


def make_trigger_response() -> Any:
    """Create a Trigger response for tests and non-ROS environments."""

    return Trigger.Response()
