import memory_aware_ros2_agent
from memory_aware_ros2_agent import EventType, MemoryEvent, TaskTrace


def test_models_are_exported_from_package_root() -> None:
    assert memory_aware_ros2_agent.MemoryEvent is MemoryEvent
    assert memory_aware_ros2_agent.TaskTrace is TaskTrace
    assert memory_aware_ros2_agent.EventType is EventType


def test_package_all_includes_model_exports() -> None:
    assert "MemoryEvent" in memory_aware_ros2_agent.__all__
    assert "TaskTrace" in memory_aware_ros2_agent.__all__
    assert "EventType" in memory_aware_ros2_agent.__all__
