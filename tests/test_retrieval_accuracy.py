from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.recall_benchmarks import small_recall_benchmark_dataset
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


def test_exact_match_recall_returns_relevant_benchmark_events() -> None:
    dataset = small_recall_benchmark_dataset()
    store = InMemoryStore()
    for trace in dataset.traces:
        store.save_trace(trace)
    for event in dataset.events:
        store.save_event(event)
    case = dataset.cases[0]

    result = ExactMatchRecallEngine().recall(case.query, store)

    assert tuple(event.event_id for event in result.events) == case.relevant_event_ids


def test_exact_match_recall_excludes_irrelevant_benchmark_events() -> None:
    dataset = small_recall_benchmark_dataset()
    store = InMemoryStore()
    for event in dataset.events:
        store.save_event(event)

    result = ExactMatchRecallEngine().recall(dataset.cases[0].query, store)

    assert "event-charge-start" not in {event.event_id for event in result.events}
