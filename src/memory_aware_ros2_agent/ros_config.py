"""Shared ROS2 node configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory_aware_ros2_agent.ros_compat import Node
from memory_aware_ros2_agent.ros_topics import (
    MEMORY_EVENTS_TOPIC,
    MEMORY_TRACES_TOPIC,
    RECALL_SERVICE_NAME,
)


@dataclass(frozen=True)
class RosNodeConfig:
    """Runtime settings shared by the ROS2 integration nodes."""

    memory_events_topic: str = MEMORY_EVENTS_TOPIC
    memory_traces_topic: str = MEMORY_TRACES_TOPIC
    recall_service_name: str = RECALL_SERVICE_NAME
    queue_depth: int = 10


def declare_ros_node_config(
    node: Node,
    defaults: RosNodeConfig | None = None,
) -> RosNodeConfig:
    """Declare common ROS parameters and return their resolved values."""

    config = defaults or RosNodeConfig()
    resolved = RosNodeConfig(
        memory_events_topic=str(
            _declare_parameter(node, "memory_events_topic", config.memory_events_topic)
        ),
        memory_traces_topic=str(
            _declare_parameter(node, "memory_traces_topic", config.memory_traces_topic)
        ),
        recall_service_name=str(
            _declare_parameter(node, "recall_service_name", config.recall_service_name)
        ),
        queue_depth=int(_declare_parameter(node, "queue_depth", config.queue_depth)),
    )
    from memory_aware_ros2_agent.ros_validation import validate_ros_node_config

    validate_ros_node_config(resolved)
    return resolved


def _declare_parameter(node: Node, name: str, default: Any) -> Any:
    parameter = node.declare_parameter(name, default)
    return getattr(parameter, "value", default)
