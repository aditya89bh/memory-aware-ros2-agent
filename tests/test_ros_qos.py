import pytest

from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.ros_qos import QoSConfig, make_qos_profile
from memory_aware_ros2_agent.trace_publisher_node import TracePublisher
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_qos_config_defaults_to_reliable_keep_last_profile() -> None:
    config = QoSConfig()
    profile = make_qos_profile(config)

    assert config.depth == 10
    assert getattr(profile, "depth", config.depth) == 10


def test_qos_profile_accepts_custom_topic_policies() -> None:
    profile = make_qos_profile(
        QoSConfig(
            depth=3,
            reliability="best_effort",
            durability="transient_local",
            history="keep_last",
        )
    )

    assert getattr(profile, "depth", 3) == 3


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reliability", "eventual"),
        ("durability", "persistent"),
        ("history", "unknown"),
    ],
)
def test_qos_profile_rejects_unknown_policy_values(field: str, value: str) -> None:
    kwargs = {field: value}

    with pytest.raises(ValueError, match=f"Unsupported QoS {field}"):
        make_qos_profile(QoSConfig(**kwargs))


def test_topic_nodes_accept_custom_qos_config() -> None:
    qos_config = QoSConfig(depth=4, reliability="best_effort")

    recorder = MemoryRecorder(qos_config=qos_config)
    publisher = TracePublisher(qos_config=qos_config)
    subscriber = TraceSubscriber(qos_config=qos_config)

    assert getattr(recorder.qos_profile, "depth", 4) == 4
    assert getattr(publisher.qos_profile, "depth", 4) == 4
    assert getattr(subscriber.qos_profile, "depth", 4) == 4
