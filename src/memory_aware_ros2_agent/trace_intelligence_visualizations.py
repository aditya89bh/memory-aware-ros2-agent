"""Text visualizations for trace intelligence outputs."""

from __future__ import annotations

from memory_aware_ros2_agent.trace_intelligence import ExperienceSummary
from memory_aware_ros2_agent.trace_intelligence_reports import (
    TraceAnalyzerBenchmarkReport,
)


def render_trace_analyzer_benchmark_report(
    report: TraceAnalyzerBenchmarkReport,
) -> str:
    """Render a benchmark report as deterministic text."""

    return "\n".join(
        (
            f"Trace Analyzer Benchmark: {report.dataset_name}",
            f"Cases: {report.case_count}",
            f"Status accuracy: {report.status_accuracy:.2f}",
            f"Failure pattern accuracy: {report.failure_pattern_accuracy:.2f}",
            f"Anomaly accuracy: {report.anomaly_accuracy:.2f}",
        )
    )


def render_experience_summary(summary: ExperienceSummary) -> str:
    """Render an experience summary as deterministic text."""

    lines = [
        f"Trace: {summary.trace_id}",
        f"Task: {summary.task_name}",
        f"Status: {summary.status}",
    ]
    lines.extend(f"- {highlight}" for highlight in summary.highlights)
    return "\n".join(lines)
