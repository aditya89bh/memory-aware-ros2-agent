import pytest

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.recall_service_node import RecallService
from memory_aware_ros2_agent.ros_callback_groups import (
    CallbackGroupConfig,
    make_callback_group,
)
from memory_aware_ros2_agent.trace_publisher_node import TracePublisher
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_callback_group_config_defaults_to_mutually_exclusive() -> None:
    config = CallbackGroupConfig()
    group = make_callback_group(config)

    assert config.kind == "mutually_exclusive"
    assert group is not None


def test_callback_group_config_accepts_reentrant_group() -> None:
    group = make_callback_group(CallbackGroupConfig(kind="reentrant"))

    assert group is not None


def test_callback_group_config_rejects_unknown_kind() -> None:
    with pytest.raises(ValueError, match="Unsupported callback group kind"):
        make_callback_group(CallbackGroupConfig(kind="parallel"))


def test_ros_nodes_accept_callback_group_config() -> None:
    config = CallbackGroupConfig(kind="reentrant")

    recorder = MemoryRecorder(callback_group_config=config)
    service = RecallService(callback_group_config=config)
    publisher = TracePublisher(callback_group_config=config)
    subscriber = TraceSubscriber(callback_group_config=config)

    assert recorder.callback_group is not None
    assert service.callback_group is not None
    assert publisher.callback_group is not None
    assert subscriber.callback_group is not None
