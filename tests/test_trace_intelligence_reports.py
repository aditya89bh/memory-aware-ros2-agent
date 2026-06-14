from memory_aware_ros2_agent.trace_intelligence_benchmarks import (
    TraceAnalyzerBenchmarkDataset,
    default_trace_analyzer_benchmark_dataset,
)
from memory_aware_ros2_agent.trace_intelligence_reports import (
    TraceAnalyzerBenchmarkReport,
    build_trace_analyzer_benchmark_report,
)


def test_build_trace_analyzer_benchmark_report_scores_default_dataset() -> None:
    dataset = default_trace_analyzer_benchmark_dataset()

    report = build_trace_analyzer_benchmark_report(dataset)

    assert report == TraceAnalyzerBenchmarkReport(
        dataset_name="default-trace-intelligence",
        case_count=3,
        status_accuracy=1.0,
        failure_pattern_accuracy=1.0,
        anomaly_accuracy=1.0,
    )


def test_build_trace_analyzer_benchmark_report_handles_empty_dataset() -> None:
    report = build_trace_analyzer_benchmark_report(
        TraceAnalyzerBenchmarkDataset("empty", ())
    )

    assert report == TraceAnalyzerBenchmarkReport("empty", 0, 0.0, 0.0, 0.0)
