"""Memory-aware ROS2 agent package."""

from memory_aware_ros2_agent._version import __version__
from memory_aware_ros2_agent.models import (
    EventMetadata,
    EventType,
    MemoryEvent,
    RecallQuery,
    RecallResult,
    SourceNode,
    TaskOutcome,
    TaskTrace,
)

PACKAGE_NAME = "memory-aware-ros2-agent"

__all__ = [
    "PACKAGE_NAME",
    "EventMetadata",
    "EventType",
    "MemoryEvent",
    "RecallQuery",
    "RecallResult",
    "SourceNode",
    "TaskOutcome",
    "TaskTrace",
    "__version__",
]
