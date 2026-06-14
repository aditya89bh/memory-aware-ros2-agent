from memory_aware_ros2_agent.cli import run_benchmarks


def test_run_benchmarks_returns_named_results() -> None:
    results = run_benchmarks(event_count=5, limit=2)

    assert [result["name"] for result in results] == [
        "load_fixture_creation",
        "exact_match_recall",
    ]
    assert all("elapsed_seconds" in result for result in results)
