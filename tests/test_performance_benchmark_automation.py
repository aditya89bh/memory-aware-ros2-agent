from memory_aware_ros2_agent.performance_benchmarks import (
    benchmark_exact_match_recall,
    benchmark_load_fixture_creation,
)


def test_benchmark_load_fixture_creation_returns_result() -> None:
    result = benchmark_load_fixture_creation(event_count=10)

    assert result.name == "load_fixture_creation"
    assert result.item_count == 10
    assert result.elapsed_seconds >= 0.0


def test_benchmark_exact_match_recall_returns_limited_result_count() -> None:
    result = benchmark_exact_match_recall(event_count=25, limit=7)

    assert result.name == "exact_match_recall"
    assert result.item_count == 7
    assert result.elapsed_seconds >= 0.0
