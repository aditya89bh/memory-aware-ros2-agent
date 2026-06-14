from memory_aware_ros2_agent.trace_intelligence import (
    detect_repeated_failures,
    detect_trace_anomalies,
    summarize_outcome,
)
from memory_aware_ros2_agent.trace_intelligence_benchmarks import (
    default_trace_analyzer_benchmark_dataset,
)


def test_default_trace_analyzer_benchmark_dataset_is_deterministic() -> None:
    dataset = default_trace_analyzer_benchmark_dataset()

    assert dataset.name == "default-trace-intelligence"
    assert tuple(case.case_id for case in dataset.cases) == (
        "successful-dock",
        "repeated-timeout",
        "failure-after-success",
    )


def test_benchmark_cases_match_expected_traits() -> None:
    dataset = default_trace_analyzer_benchmark_dataset()

    for case in dataset.cases:
        assert summarize_outcome(case.trace).status == case.expected_status
        repeated_reasons = tuple(
            failure.reason for failure in detect_repeated_failures(case.trace)
        )
        anomaly_types = tuple(
            anomaly.anomaly_type
            for anomaly in detect_trace_anomalies(
                case.trace, require_terminal_event=False
            )
        )
        assert repeated_reasons == case.expected_failure_reasons
        assert anomaly_types == case.expected_anomaly_types
