"""ROS2 node exposing a recall service interface."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.ros_callback_groups import (
    CallbackGroupConfig,
    make_callback_group,
)
from memory_aware_ros2_agent.ros_compat import Node, Trigger
from memory_aware_ros2_agent.ros_config import (
    RosNodeConfig,
    declare_ros_node_config,
    namespace_for_node,
)


class RecallService(Node):
    """Expose a recall service placeholder without implementing recall algorithms."""

    def __init__(
        self,
        config: RosNodeConfig | None = None,
        callback_group_config: CallbackGroupConfig | None = None,
    ) -> None:
        super().__init__("recall_service", namespace=namespace_for_node(config))
        self.config = declare_ros_node_config(self, config)
        self.callback_group = make_callback_group(callback_group_config)
        self.create_service(
            Trigger,
            self.config.recall_service_name,
            self.handle_recall,
            callback_group=self.callback_group,
        )

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
        node.destroy_node()
        rclpy.shutdown()


def make_trigger_response() -> Any:
    """Create a Trigger response for tests and non-ROS environments."""

    return Trigger.Response()
