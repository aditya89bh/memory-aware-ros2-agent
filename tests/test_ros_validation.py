import pytest

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_config import RosNodeConfig
from memory_aware_ros2_agent.ros_validation import validate_ros_node_config


def test_validate_ros_node_config_accepts_defaults() -> None:
    validate_ros_node_config(RosNodeConfig())


@pytest.mark.parametrize(
    "config",
    [
        RosNodeConfig(memory_events_topic=""),
        RosNodeConfig(memory_traces_topic=" "),
        RosNodeConfig(recall_service_name=""),
        RosNodeConfig(queue_depth=0),
    ],
)
def test_validate_ros_node_config_rejects_invalid_startup_config(
    config: RosNodeConfig,
) -> None:
    with pytest.raises(ValueError):
        validate_ros_node_config(config)


def test_nodes_validate_config_at_startup() -> None:
    with pytest.raises(ValueError, match="queue_depth"):
        MemoryRecorder(RosNodeConfig(queue_depth=0))
