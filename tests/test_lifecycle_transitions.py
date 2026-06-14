from memory_aware_ros2_agent.lifecycle_node import MemoryLifecycleNode
from memory_aware_ros2_agent.ros_compat import (
    DiagnosticStatus,
    TransitionCallbackReturn,
)


def test_lifecycle_transition_sequence_updates_state_and_diagnostics() -> None:
    node = MemoryLifecycleNode()

    assert node.diagnostic_status().level == DiagnosticStatus.WARN

    assert node.on_configure(None) == TransitionCallbackReturn.SUCCESS
    configured_status = node.diagnostic_status()
    assert node.is_configured is True
    assert configured_status.level == DiagnosticStatus.OK
    assert configured_status.message == "inactive"

    assert node.on_activate(None) == TransitionCallbackReturn.SUCCESS
    active_status = node.diagnostic_status()
    assert node.is_active is True
    assert active_status.message == "active"

    assert node.on_deactivate(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_active is False

    assert node.on_cleanup(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_configured is False
    assert node.diagnostic_status().level == DiagnosticStatus.WARN


def test_lifecycle_shutdown_keeps_node_configured_but_inactive() -> None:
    node = MemoryLifecycleNode()
    node.on_configure(None)
    node.on_activate(None)

    assert node.on_shutdown(None) == TransitionCallbackReturn.SUCCESS

    assert node.is_configured is True
    assert node.is_active is False
    assert node.diagnostic_status().message == "inactive"
