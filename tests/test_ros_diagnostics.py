from memory_aware_ros2_agent.lifecycle_node import MemoryLifecycleNode
from memory_aware_ros2_agent.ros_compat import DiagnosticStatus
from memory_aware_ros2_agent.ros_diagnostics import (
    DiagnosticConfig,
    make_diagnostic_status,
    make_key_value,
)


def test_make_key_value_converts_values_to_strings() -> None:
    value = make_key_value("active", True)

    assert value.key == "active"
    assert value.value == "True"


def test_make_diagnostic_status_builds_ok_status() -> None:
    status = make_diagnostic_status(
        name="memory_lifecycle",
        message="active",
        values={"configured": True},
        config=DiagnosticConfig(hardware_id="robot-1"),
    )

    assert status.level == DiagnosticStatus.OK
    assert status.hardware_id == "robot-1"
    assert status.values[0].key == "configured"


def test_make_diagnostic_status_builds_warning_status() -> None:
    status = make_diagnostic_status(
        name="memory_lifecycle",
        message="inactive",
        ok=False,
    )

    assert status.level == DiagnosticStatus.WARN


def test_lifecycle_node_returns_diagnostic_status() -> None:
    node = MemoryLifecycleNode()

    inactive_status = node.diagnostic_status()
    node.on_configure(None)
    node.on_activate(None)
    active_status = node.diagnostic_status()

    assert inactive_status.level == DiagnosticStatus.WARN
    assert active_status.level == DiagnosticStatus.OK
    assert active_status.message == "active"
