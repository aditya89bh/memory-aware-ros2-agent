"""ROS2 QoS profile configuration helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory_aware_ros2_agent.ros_compat import (
    DurabilityPolicy,
    HistoryPolicy,
    QoSProfile,
    ReliabilityPolicy,
)


@dataclass(frozen=True)
class QoSConfig:
    """Serializable QoS settings for ROS2 topic endpoints."""

    depth: int = 10
    reliability: str = "reliable"
    durability: str = "volatile"
    history: str = "keep_last"


def make_qos_profile(config: QoSConfig | None = None) -> QoSProfile:
    """Build a ROS2 QoS profile from stable string configuration values."""

    resolved = config or QoSConfig()
    return QoSProfile(
        depth=resolved.depth,
        reliability=_reliability_policy(resolved.reliability),
        durability=_durability_policy(resolved.durability),
        history=_history_policy(resolved.history),
    )


def _reliability_policy(value: str) -> Any:
    if value == "reliable":
        return ReliabilityPolicy.RELIABLE
    if value == "best_effort":
        return ReliabilityPolicy.BEST_EFFORT
    msg = f"Unsupported QoS reliability: {value}"
    raise ValueError(msg)


def _durability_policy(value: str) -> Any:
    if value == "volatile":
        return DurabilityPolicy.VOLATILE
    if value == "transient_local":
        return DurabilityPolicy.TRANSIENT_LOCAL
    msg = f"Unsupported QoS durability: {value}"
    raise ValueError(msg)


def _history_policy(value: str) -> Any:
    if value == "keep_last":
        return HistoryPolicy.KEEP_LAST
    if value == "keep_all":
        return HistoryPolicy.KEEP_ALL
    msg = f"Unsupported QoS history: {value}"
    raise ValueError(msg)
