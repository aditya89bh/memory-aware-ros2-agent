from memory_aware_ros2_agent.lifecycle_node import MemoryLifecycleNode
from memory_aware_ros2_agent.ros_compat import TransitionCallbackReturn
from memory_aware_ros2_agent.ros_config import RosNodeConfig


def test_lifecycle_node_accepts_shared_config() -> None:
    node = MemoryLifecycleNode(
        config=RosNodeConfig(memory_events_topic="robot/memory/events")
    )

    assert node.config.memory_events_topic == "robot/memory/events"


def test_lifecycle_node_tracks_transition_state() -> None:
    node = MemoryLifecycleNode()

    assert node.is_configured is False
    assert node.is_active is False

    assert node.on_configure(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_configured is True

    assert node.on_activate(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_active is True

    assert node.on_deactivate(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_active is False

    assert node.on_cleanup(None) == TransitionCallbackReturn.SUCCESS
    assert node.is_configured is False


def test_lifecycle_node_shutdown_deactivates_node() -> None:
    node = MemoryLifecycleNode()
    node.on_configure(None)
    node.on_activate(None)

    assert node.on_shutdown(None) == TransitionCallbackReturn.SUCCESS

    assert node.is_active is False
