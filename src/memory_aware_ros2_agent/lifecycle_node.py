"""ROS2 lifecycle node support for memory-aware agents."""

from __future__ import annotations

from typing import Any

from memory_aware_ros2_agent.ros_compat import (
    DiagnosticStatus,
    LifecycleNode,
    TransitionCallbackReturn,
)
from memory_aware_ros2_agent.ros_config import (
    RosNodeConfig,
    declare_ros_node_config,
    namespace_for_node,
)
from memory_aware_ros2_agent.ros_diagnostics import make_diagnostic_status
from memory_aware_ros2_agent.ros_logging import log_info


class MemoryLifecycleNode(LifecycleNode):
    """Lifecycle-aware base node for memory integration components."""

    def __init__(
        self,
        node_name: str = "memory_lifecycle",
        config: RosNodeConfig | None = None,
    ) -> None:
        super().__init__(node_name, namespace=namespace_for_node(config))
        self.config = declare_ros_node_config(self, config)
        self.is_configured = False
        self.is_active = False

    def on_configure(self, _state: Any) -> Any:
        """Mark the lifecycle node as configured."""

        self.is_configured = True
        log_info(self.get_logger(), "lifecycle_configured")
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, _state: Any) -> Any:
        """Mark the lifecycle node as active."""

        self.is_active = True
        log_info(self.get_logger(), "lifecycle_activated")
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, _state: Any) -> Any:
        """Mark the lifecycle node as inactive."""

        self.is_active = False
        log_info(self.get_logger(), "lifecycle_deactivated")
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, _state: Any) -> Any:
        """Reset configured and active state."""

        self.is_active = False
        self.is_configured = False
        log_info(self.get_logger(), "lifecycle_cleaned_up")
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, _state: Any) -> Any:
        """Mark the lifecycle node as shut down."""

        self.is_active = False
        log_info(self.get_logger(), "lifecycle_shutdown")
        return TransitionCallbackReturn.SUCCESS

    def diagnostic_status(self) -> DiagnosticStatus:
        """Return a diagnostic snapshot for lifecycle state."""

        return make_diagnostic_status(
            name=self.get_name(),
            message="active" if self.is_active else "inactive",
            ok=self.is_configured,
            values={
                "configured": self.is_configured,
                "active": self.is_active,
                "namespace": self.config.namespace,
            },
        )


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
