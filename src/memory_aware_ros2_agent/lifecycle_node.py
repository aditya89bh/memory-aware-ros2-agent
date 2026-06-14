"""ROS2 lifecycle node support for memory-aware agents."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.ros_compat import (
    LifecycleNode,
    TransitionCallbackReturn,
)
from memory_aware_ros2_agent.ros_config import RosNodeConfig, declare_ros_node_config


class MemoryLifecycleNode(LifecycleNode):
    """Lifecycle-aware base node for memory integration components."""

    def __init__(
        self,
        node_name: str = "memory_lifecycle",
        config: RosNodeConfig | None = None,
    ) -> None:
        super().__init__(node_name)
        self.config = declare_ros_node_config(self, config)
        self.is_configured = False
        self.is_active = False

    def on_configure(self, _state: Any) -> Any:
        """Mark the lifecycle node as configured."""

        self.is_configured = True
        self.get_logger().info("Configured memory lifecycle node")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, _state: Any) -> Any:
        """Mark the lifecycle node as active."""

        self.is_active = True
        self.get_logger().info("Activated memory lifecycle node")
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, _state: Any) -> Any:
        """Mark the lifecycle node as inactive."""

        self.is_active = False
        self.get_logger().info("Deactivated memory lifecycle node")
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, _state: Any) -> Any:
        """Reset configured and active state."""

        self.is_active = False
        self.is_configured = False
        self.get_logger().info("Cleaned up memory lifecycle node")
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, _state: Any) -> Any:
        """Mark the lifecycle node as shut down."""

        self.is_active = False
        self.get_logger().info("Shut down memory lifecycle node")
        return TransitionCallbackReturn.SUCCESS


def main() -> None:
    """Run the memory lifecycle node."""

    from memory_aware_ros2_agent.ros_compat import rclpy

    if rclpy is None:
        raise RuntimeError("rclpy is required to run MemoryLifecycleNode")

    rclpy.init()
    node = MemoryLifecycleNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
