"""ROS2 node for publishing serialized task traces."""

from __future__ import annotations

import json
from typing import Any

from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.ros_callback_groups import (
    CallbackGroupConfig,
    make_callback_group,
)
from memory_aware_ros2_agent.ros_compat import Node, String
from memory_aware_ros2_agent.ros_config import RosNodeConfig, declare_ros_node_config
from memory_aware_ros2_agent.ros_qos import QoSConfig, make_qos_profile
from memory_aware_ros2_agent.serialization import model_to_dict


class TracePublisher(Node):
    """Publish task traces as JSON strings."""

    def __init__(
        self,
        config: RosNodeConfig | None = None,
        qos_config: QoSConfig | None = None,
        callback_group_config: CallbackGroupConfig | None = None,
    ) -> None:
        super().__init__("trace_publisher")
        self.config = declare_ros_node_config(self, config)
        self.qos_profile = make_qos_profile(
            qos_config or QoSConfig(depth=self.config.queue_depth)
        )
        self.callback_group = make_callback_group(callback_group_config)
        self.publisher = self.create_publisher(
            String,
            self.config.memory_traces_topic,
            self.qos_profile,
            callback_group=self.callback_group,
        )

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
