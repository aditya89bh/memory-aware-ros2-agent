from memory_aware_ros2_agent.id_utils import (
    new_event_id,
    new_id,
    new_query_id,
    new_trace_id,
)


def test_new_id_uses_normalized_prefix() -> None:
    identifier = new_id("Task_Event")

    assert identifier.startswith("task-event-")


def test_specific_id_helpers_use_stable_prefixes() -> None:
    assert new_event_id().startswith("event-")
    assert new_trace_id().startswith("trace-")
    assert new_query_id().startswith("query-")


def test_new_id_rejects_empty_prefix() -> None:
    try:
        new_id("  ")
    except ValueError as exc:
        assert "prefix" in str(exc)
    else:
        raise AssertionError("Expected empty prefix to raise ValueError")
