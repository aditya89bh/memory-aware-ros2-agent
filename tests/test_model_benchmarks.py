from time import perf_counter

from memory_aware_ros2_agent.factories import create_memory_event
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.serialization import model_to_dict


def test_memory_event_creation_is_lightweight() -> None:
    start = perf_counter()

    events = [
        create_memory_event(
            trace_id="trace-001",
            event_type=EventType.TASK_OBSERVED,
            summary="Robot observed workspace.",
        )
        for _ in range(1_000)
    ]

    elapsed = perf_counter() - start
    assert len(events) == 1_000
    assert elapsed < 2.0


def test_memory_event_serialization_is_lightweight() -> None:
    events = [
        create_memory_event(
            trace_id="trace-001",
            event_type=EventType.TASK_OBSERVED,
            summary="Robot observed workspace.",
        )
        for _ in range(1_000)
    ]

    start = perf_counter()
    serialized = [model_to_dict(event) for event in events]
    elapsed = perf_counter() - start

    assert len(serialized) == 1_000
    assert elapsed < 2.0
