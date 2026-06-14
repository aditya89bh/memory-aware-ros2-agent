from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_config import RosNodeConfig, namespace_for_node
from memory_aware_ros2_agent.ros_topics import normalize_namespace


def test_normalize_namespace_allows_global_default() -> None:
    assert normalize_namespace("") == ""
    assert normalize_namespace("  ") == ""


def test_normalize_namespace_returns_absolute_namespace() -> None:
    assert normalize_namespace("robot/memory") == "/robot/memory"
    assert normalize_namespace("/robot//memory") == "/robot/memory"


def test_namespace_for_node_returns_none_for_default_namespace() -> None:
    assert namespace_for_node(RosNodeConfig()) is None


def test_namespace_for_node_returns_normalized_namespace() -> None:
    assert namespace_for_node(RosNodeConfig(namespace="robot")) == "/robot"


def test_nodes_accept_namespace_config() -> None:
    node = MemoryRecorder(RosNodeConfig(namespace="robot"))

    if hasattr(node, "get_namespace"):
        assert node.get_namespace() == "/robot"
    else:
        assert node.namespace == "/robot"
    assert node.config.namespace == "/robot"
