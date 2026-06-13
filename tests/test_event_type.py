from memory_aware_ros2_agent.models import EventType


def test_event_type_values_are_stable_strings() -> None:
    assert EventType.TASK_STARTED.value == "task.started"
    assert EventType.TASK_OBSERVED.value == "task.observed"
    assert EventType.TASK_DECIDED.value == "task.decided"
    assert EventType.TASK_ACTED.value == "task.acted"
    assert EventType.TASK_FAILED.value == "task.failed"
    assert EventType.TASK_SUCCEEDED.value == "task.succeeded"
