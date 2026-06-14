from concurrent.futures import ThreadPoolExecutor

from memory_aware_ros2_agent.factories import create_memory_event, create_task_trace
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType


def test_concurrent_save_delete_cycles_leave_store_consistent() -> None:
    store = InMemoryStore()
    event = create_memory_event(
        trace_id="trace-threaded",
        event_type=EventType.TASK_OBSERVED,
        summary="Threaded observation",
        event_id="event-threaded",
    )

    def save_and_delete() -> None:
        store.save_event(event)
        store.delete_event(event.event_id)

    with ThreadPoolExecutor(max_workers=8) as executor:
        tuple(executor.map(lambda _index: save_and_delete(), range(100)))

    assert store.get_event(event.event_id) is None


def test_concurrent_trace_reads_see_complete_snapshots() -> None:
    store = InMemoryStore()
    traces = tuple(
        create_task_trace(
            task_name="threaded-task",
            trace_id=f"trace-{index}",
        )
        for index in range(20)
    )
    for trace in traces:
        store.save_trace(trace)

    with ThreadPoolExecutor(max_workers=4) as executor:
        snapshots = tuple(executor.map(lambda _index: store.list_traces(), range(20)))

    assert all(len(snapshot) == 20 for snapshot in snapshots)
    expected_trace_ids = {f"trace-{index}" for index in range(20)}
    assert all(
        {trace.trace_id for trace in snapshot} == expected_trace_ids
        for snapshot in snapshots
    )
