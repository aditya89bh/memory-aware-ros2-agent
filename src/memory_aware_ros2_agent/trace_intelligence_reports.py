"""Benchmark reporting for trace intelligence analyzers."""

from __future__ import annotations

from dataclasses import dataclass

from memory_aware_ros2_agent.trace_intelligence import (
    detect_repeated_failures,
    detect_trace_anomalies,
    summarize_outcome,
)
from memory_aware_ros2_agent.trace_intelligence_benchmarks import (
    TraceAnalyzerBenchmarkDataset,
)


@dataclass(frozen=True)
class TraceAnalyzerBenchmarkReport:
    """Aggregate report for a trace analyzer benchmark dataset."""

    dataset_name: str
    case_count: int
    status_accuracy: float
    failure_pattern_accuracy: float
    anomaly_accuracy: float


def build_trace_analyzer_benchmark_report(
    dataset: TraceAnalyzerBenchmarkDataset,
) -> TraceAnalyzerBenchmarkReport:
    """Evaluate benchmark expectations against analyzer outputs."""

    if not dataset.cases:
        return TraceAnalyzerBenchmarkReport(dataset.name, 0, 0.0, 0.0, 0.0)

    status_matches = 0
    failure_matches = 0
    anomaly_matches = 0
    for case in dataset.cases:
        if summarize_outcome(case.trace).status == case.expected_status:
            status_matches += 1
        failure_reasons = tuple(
            failure.reason for failure in detect_repeated_failures(case.trace)
        )
        if failure_reasons == case.expected_failure_reasons:
            failure_matches += 1
        anomaly_types = tuple(
            anomaly.anomaly_type
            for anomaly in detect_trace_anomalies(
                case.trace, require_terminal_event=False
            )
        )
        if anomaly_types == case.expected_anomaly_types:
            anomaly_matches += 1

    case_count = len(dataset.cases)
    return TraceAnalyzerBenchmarkReport(
        dataset_name=dataset.name,
        case_count=case_count,
        status_accuracy=status_matches / case_count,
        failure_pattern_accuracy=failure_matches / case_count,
        anomaly_accuracy=anomaly_matches / case_count,
    )
