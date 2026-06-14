import tracemalloc

from memory_aware_ros2_agent.factories import create_memory_event
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType


def test_in_memory_store_bulk_event_usage_stays_bounded() -> None:
    tracemalloc.start()
    try:
        store = InMemoryStore()
        for index in range(1_000):
            store.save_event(
                create_memory_event(
                    trace_id="trace-memory",
                    event_type=EventType.TASK_OBSERVED,
                    summary=f"Memory observation {index}",
                    event_id=f"event-{index}",
                    payload={"index": index},
                )
            )
        _current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert len(store.list_events()) == 1_000
    assert peak_bytes < 2_000_000
