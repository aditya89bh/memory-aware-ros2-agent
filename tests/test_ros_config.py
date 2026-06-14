from memory_aware_ros2_agent.memory_recorder_node import MemoryRecorder
from memory_aware_ros2_agent.recall_service_node import RecallService
from memory_aware_ros2_agent.ros_config import RosNodeConfig
from memory_aware_ros2_agent.trace_publisher_node import TracePublisher
from memory_aware_ros2_agent.trace_subscriber_node import TraceSubscriber


def test_ros_node_config_defaults_match_existing_interfaces() -> None:
    config = RosNodeConfig()

    assert config.memory_events_topic == "memory/events"
    assert config.memory_traces_topic == "memory/traces"
    assert config.recall_service_name == "memory/recall"
    assert config.queue_depth == 10


def test_memory_recorder_accepts_parameter_config() -> None:
    node = MemoryRecorder(
        RosNodeConfig(memory_events_topic="robot/memory/events", queue_depth=5)
    )

    assert node.config.memory_events_topic == "robot/memory/events"
    assert node.config.queue_depth == 5


def test_recall_service_accepts_parameter_config() -> None:
    node = RecallService(RosNodeConfig(recall_service_name="robot/memory/recall"))

    assert node.config.recall_service_name == "robot/memory/recall"


def test_trace_nodes_accept_parameter_config() -> None:
    config = RosNodeConfig(memory_traces_topic="robot/memory/traces", queue_depth=7)

    publisher = TracePublisher(config)
    subscriber = TraceSubscriber(config)

    assert publisher.config.memory_traces_topic == "robot/memory/traces"
    assert subscriber.config.memory_traces_topic == "robot/memory/traces"
    assert publisher.config.queue_depth == 7
    assert subscriber.config.queue_depth == 7
