from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_compat import (
    DurabilityPolicy,
    HistoryPolicy,
    ReliabilityPolicy,
)
from memory_aware_ros2_agent.ros_config import RosNodeConfig
from memory_aware_ros2_agent.ros_qos import QoSConfig, make_qos_profile
from memory_aware_ros2_agent.trace_publisher_node import TracePublisher
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_default_qos_profile_uses_reliable_volatile_keep_last() -> None:
    profile = make_qos_profile()

    assert profile.depth == 10
    assert profile.reliability == ReliabilityPolicy.RELIABLE
    assert profile.durability == DurabilityPolicy.VOLATILE
    assert profile.history == HistoryPolicy.KEEP_LAST


def test_qos_profile_supports_best_effort_transient_local() -> None:
    profile = make_qos_profile(
        QoSConfig(
            depth=2,
            reliability="best_effort",
            durability="transient_local",
        )
    )

    assert profile.depth == 2
    assert profile.reliability == ReliabilityPolicy.BEST_EFFORT
    assert profile.durability == DurabilityPolicy.TRANSIENT_LOCAL


def test_qos_profile_supports_keep_all_history() -> None:
    profile = make_qos_profile(QoSConfig(history="keep_all"))

    assert profile.history == HistoryPolicy.KEEP_ALL


def test_topic_nodes_default_qos_depth_from_node_config() -> None:
    config = RosNodeConfig(queue_depth=6)

    recorder = MemoryRecorder(config)
    publisher = TracePublisher(config)
    subscriber = TraceSubscriber(config)

    assert recorder.qos_profile.depth == 6
    assert publisher.qos_profile.depth == 6
    assert subscriber.qos_profile.depth == 6
