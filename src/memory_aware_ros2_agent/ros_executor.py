"""Executor utility helpers for ROS2 nodes."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from memory_aware_ros2_agent.ros_compat import (
    MultiThreadedExecutor,
    Node,
    SingleThreadedExecutor,
)


@dataclass(frozen=True)
class ExecutorConfig:
    """Runtime settings for selecting a ROS2 executor."""

    kind: str = "single_threaded"
    num_threads: int | None = None


def make_executor(config: ExecutorConfig | None = None) -> Any:
    """Create a ROS2 executor from stable string configuration."""

    resolved = config or ExecutorConfig()
    if resolved.kind == "single_threaded":
        return SingleThreadedExecutor()
    if resolved.kind == "multi_threaded":
        return MultiThreadedExecutor(num_threads=resolved.num_threads)
    msg = f"Unsupported executor kind: {resolved.kind}"
    raise ValueError(msg)


def add_nodes(executor: Any, nodes: Iterable[Node]) -> None:
    """Add multiple nodes to an executor."""

    for node in nodes:
        executor.add_node(node)


def spin_nodes(nodes: Iterable[Node], config: ExecutorConfig | None = None) -> None:
    """Spin nodes with a managed executor until interrupted by ROS shutdown."""

    executor = make_executor(config)
    add_nodes(executor, nodes)
    try:
        executor.spin()
    finally:
        executor.shutdown()
