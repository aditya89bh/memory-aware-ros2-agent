import pytest

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_config import RosNodeConfig, declare_ros_node_config


class Parameter:
    def __init__(self, value: object) -> None:
        self.value = value


class ParameterNode:
    def __init__(self, overrides: dict[str, object] | None = None) -> None:
        self.overrides = overrides or {}
        self.declared: dict[str, object] = {}

    def declare_parameter(self, name: str, value: object) -> Parameter:
        resolved = self.overrides.get(name, value)
        self.declared[name] = resolved
        return Parameter(resolved)


def test_declare_ros_node_config_declares_all_supported_parameters() -> None:
    node = ParameterNode()

    config = declare_ros_node_config(node)

    assert config == RosNodeConfig()
    assert set(node.declared) == {
        "memory_events_topic",
        "memory_traces_topic",
        "namespace",
        "queue_depth",
        "recall_service_name",
    }


def test_declare_ros_node_config_uses_parameter_overrides() -> None:
    node = ParameterNode(
        {
            "memory_events_topic": "robot/events",
            "memory_traces_topic": "robot/traces",
            "recall_service_name": "robot/recall",
            "queue_depth": 3,
            "namespace": "robot",
        }
    )

    config = declare_ros_node_config(node)

    assert config.memory_events_topic == "robot/events"
    assert config.memory_traces_topic == "robot/traces"
    assert config.recall_service_name == "robot/recall"
    assert config.queue_depth == 3
    assert config.namespace == "/robot"


def test_declare_ros_node_config_rejects_invalid_parameter_overrides() -> None:
    node = ParameterNode({"queue_depth": -1})

    with pytest.raises(ValueError, match="queue_depth"):
        declare_ros_node_config(node)


def test_node_config_sets_runtime_parameter_values() -> None:
    node = MemoryRecorder(RosNodeConfig(memory_events_topic="robot/events"))

    assert node.config.memory_events_topic == "robot/events"
