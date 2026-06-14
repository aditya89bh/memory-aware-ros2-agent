"""Startup validation helpers for ROS2 integration nodes."""

from __future__ import annotations

from memory_aware_ros2_agent.ros_config import RosNodeConfig


def validate_ros_node_config(config: RosNodeConfig) -> None:
    """Validate shared ROS node configuration before creating entities."""

    _require_non_empty("memory_events_topic", config.memory_events_topic)
    _require_non_empty("memory_traces_topic", config.memory_traces_topic)
    _require_non_empty("recall_service_name", config.recall_service_name)
    if config.queue_depth <= 0:
        msg = "queue_depth must be greater than zero"
        raise ValueError(msg)


def _require_non_empty(field_name: str, value: str) -> None:
    if not value.strip():
        msg = f"{field_name} must not be empty"
        raise ValueError(msg)
