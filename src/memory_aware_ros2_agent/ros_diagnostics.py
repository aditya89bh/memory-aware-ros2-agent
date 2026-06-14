"""ROS2 diagnostics helpers for memory-aware nodes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from memory_aware_ros2_agent.ros_compat import DiagnosticStatus, KeyValue


@dataclass(frozen=True)
class DiagnosticConfig:
    """Shared diagnostic metadata."""

    hardware_id: str = "memory-aware-ros2-agent"


def make_key_value(key: str, value: Any) -> KeyValue:
    """Create a ROS diagnostic key/value pair."""

    return KeyValue(key=str(key), value=str(value))


def make_diagnostic_status(
    *,
    name: str,
    message: str,
    ok: bool = True,
    values: dict[str, Any] | None = None,
    config: DiagnosticConfig | None = None,
) -> DiagnosticStatus:
    """Create a ROS diagnostic status message."""

    diagnostic_config = config or DiagnosticConfig()
    status = DiagnosticStatus()
    status.level = DiagnosticStatus.OK if ok else DiagnosticStatus.WARN
    status.name = name
    status.message = message
    status.hardware_id = diagnostic_config.hardware_id
    status.values = [
        make_key_value(key, value) for key, value in (values or {}).items()
    ]
    return status
