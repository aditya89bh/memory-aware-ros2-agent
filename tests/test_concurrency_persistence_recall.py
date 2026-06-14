from concurrent.futures import ThreadPoolExecutor

from memory_aware_ros2_agent.factories import create_memory_event, create_recall_query
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import EventType
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


def test_concurrent_event_persistence_records_all_events() -> None:
    store = InMemoryStore()
    events = tuple(
        create_memory_event(
            trace_id="trace-concurrent",
            event_type=EventType.TASK_OBSERVED,
            summary=f"Observed marker {index}",
            event_id=f"event-{index}",
        )
        for index in range(50)
    )

    with ThreadPoolExecutor(max_workers=8) as executor:
        tuple(executor.map(store.save_event, events))

    assert {event.event_id for event in store.list_events()} == {
        f"event-{index}" for index in range(50)
    }


def test_concurrent_recall_reads_return_consistent_results() -> None:
    store = InMemoryStore()
    for index in range(20):
        store.save_event(
            create_memory_event(
                trace_id="trace-recall",
                event_type=EventType.TASK_OBSERVED,
                summary=f"Docking observation {index}",
                event_id=f"event-{index}",
            )
        )
    engine = ExactMatchRecallEngine()
    queries = tuple(
        create_recall_query(
            query_text="docking",
            query_id=f"query-{index}",
            trace_id="trace-recall",
            limit=20,
        )
        for index in range(10)
    )

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = tuple(
            executor.map(lambda query: engine.recall(query, store), queries)
        )

    assert all(len(result.events) == 20 for result in results)
    assert {result.query_id for result in results} == {
        f"query-{index}" for index in range(10)
    }
