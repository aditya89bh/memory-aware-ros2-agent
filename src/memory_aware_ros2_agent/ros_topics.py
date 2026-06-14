"""Topic and service naming conventions for ROS2 memory nodes."""

from __future__ import annotations

MEMORY_NAMESPACE = "memory"
MEMORY_EVENTS_TOPIC = f"{MEMORY_NAMESPACE}/events"
MEMORY_TRACES_TOPIC = f"{MEMORY_NAMESPACE}/traces"
RECALL_SERVICE_NAME = f"{MEMORY_NAMESPACE}/recall"


def normalize_namespace(namespace: str) -> str:
    """Normalize a ROS namespace for node construction."""

    stripped = namespace.strip()
    if not stripped:
        return ""
    normalized = normalize_ros_name(stripped)
    return normalized if normalized.startswith("/") else f"/{normalized}"


def normalize_ros_name(name: str) -> str:
    """Normalize a relative ROS graph name while preserving absolute names."""

    stripped = name.strip()
    if not stripped:
        msg = "ROS graph name must not be empty"
        raise ValueError(msg)
    if stripped == "/":
        msg = "ROS graph name must identify a topic or service"
        raise ValueError(msg)
    absolute = stripped.startswith("/")
    parts = [part for part in stripped.split("/") if part]
    normalized = "/".join(parts)
    if not normalized:
        msg = "ROS graph name must identify a topic or service"
        raise ValueError(msg)
    return f"/{normalized}" if absolute else normalized


def memory_topic(name: str) -> str:
    """Build a relative topic name under the memory namespace."""

    return normalize_ros_name(f"{MEMORY_NAMESPACE}/{name}")
