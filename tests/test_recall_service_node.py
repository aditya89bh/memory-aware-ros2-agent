from memory_aware_ros2_agent.recall_service_node import (
    RecallService,
    make_trigger_response,
)
from memory_aware_ros2_agent.ros_compat import Trigger


def test_recall_service_returns_placeholder_response() -> None:
    node = RecallService()
    response = make_trigger_response()

    result = node.handle_recall(Trigger.Request(), response)

    assert result.success is False
    assert result.message == "Recall algorithms are not implemented yet."
