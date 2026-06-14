"""ROS2 callback group configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory_aware_ros2_agent.ros_compat import (
    MutuallyExclusiveCallbackGroup,
    ReentrantCallbackGroup,
)


@dataclass(frozen=True)
class CallbackGroupConfig:
    """Runtime callback group settings for ROS2 entities."""

    kind: str = "mutually_exclusive"


def make_callback_group(config: CallbackGroupConfig | None = None) -> Any:
    """Build a ROS2 callback group from stable string configuration values."""

    resolved = config or CallbackGroupConfig()
    if resolved.kind == "mutually_exclusive":
        return MutuallyExclusiveCallbackGroup()
    if resolved.kind == "reentrant":
        return ReentrantCallbackGroup()
    msg = f"Unsupported callback group kind: {resolved.kind}"
    raise ValueError(msg)
