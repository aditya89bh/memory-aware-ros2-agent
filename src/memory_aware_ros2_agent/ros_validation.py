"""Startup validation helpers for ROS2 integration nodes."""

from __future__ import annotations

from memory_aware_ros2_agent.ros_config import RosNodeConfig
from memory_aware_ros2_agent.ros_topics import normalize_namespace, normalize_ros_name


def validate_ros_node_config(config: RosNodeConfig) -> None:
    """Validate shared ROS node configuration before creating entities."""

    normalize_ros_name(config.memory_events_topic)
    normalize_ros_name(config.memory_traces_topic)
    normalize_ros_name(config.recall_service_name)
    normalize_namespace(config.namespace)
    if config.queue_depth <= 0:
        msg = "queue_depth must be greater than zero"
        raise ValueError(msg)
