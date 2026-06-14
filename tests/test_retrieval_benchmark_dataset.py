from memory_aware_ros2_agent.recall_benchmarks import (
    small_recall_benchmark_dataset,
)


def test_small_recall_benchmark_dataset_contains_labeled_cases() -> None:
    dataset = small_recall_benchmark_dataset()

    assert len(dataset.events) == 3
    assert len(dataset.traces) == 2
    assert dataset.cases[0].relevant_event_ids == (
        "event-dock-start",
        "event-dock-failed",
    )


def test_small_recall_benchmark_dataset_case_ids_reference_events() -> None:
    dataset = small_recall_benchmark_dataset()
    event_ids = {event.event_id for event in dataset.events}

    for case in dataset.cases:
        assert set(case.relevant_event_ids).issubset(event_ids)
