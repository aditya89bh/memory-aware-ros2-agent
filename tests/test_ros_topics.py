import pytest

from memory_aware_ros2_agent.ros_config import RosNodeConfig
from memory_aware_ros2_agent.ros_topics import (
    MEMORY_EVENTS_TOPIC,
    MEMORY_TRACES_TOPIC,
    RECALL_SERVICE_NAME,
    memory_topic,
    normalize_ros_name,
)


def test_memory_topic_constants_match_default_config() -> None:
    config = RosNodeConfig()

    assert config.memory_events_topic == MEMORY_EVENTS_TOPIC
    assert config.memory_traces_topic == MEMORY_TRACES_TOPIC
    assert config.recall_service_name == RECALL_SERVICE_NAME


@pytest.mark.parametrize(
    ("raw_name", "normalized"),
    [
        ("memory/events", "memory/events"),
        (" memory//events ", "memory/events"),
        ("/robot//memory/events", "/robot/memory/events"),
    ],
)
def test_normalize_ros_name_collapses_extra_slashes(
    raw_name: str,
    normalized: str,
) -> None:
    assert normalize_ros_name(raw_name) == normalized


def test_normalize_ros_name_rejects_empty_names() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        normalize_ros_name(" ")


def test_memory_topic_builds_names_under_memory_namespace() -> None:
    assert memory_topic("events") == "memory/events"
