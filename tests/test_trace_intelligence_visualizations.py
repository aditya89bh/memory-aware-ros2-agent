from memory_aware_ros2_agent.trace_intelligence import ExperienceSummary
from memory_aware_ros2_agent.trace_intelligence_reports import (
    TraceAnalyzerBenchmarkReport,
)
from memory_aware_ros2_agent.trace_intelligence_visualizations import (
    render_experience_summary,
    render_trace_analyzer_benchmark_report,
)


def test_render_trace_analyzer_benchmark_report_outputs_stable_text() -> None:
    report = TraceAnalyzerBenchmarkReport("dataset", 2, 0.5, 1.0, 0.0)

    assert render_trace_analyzer_benchmark_report(report) == "\n".join(
        (
            "Trace Analyzer Benchmark: dataset",
            "Cases: 2",
            "Status accuracy: 0.50",
            "Failure pattern accuracy: 1.00",
            "Anomaly accuracy: 0.00",
        )
    )


def test_render_experience_summary_outputs_highlights() -> None:
    summary = ExperienceSummary(
        trace_id="trace-001",
        task_name="dock",
        status="succeeded",
        highlights=("Task dock succeeded.", "Recorded 3 events."),
    )

    assert render_experience_summary(summary) == "\n".join(
        (
            "Trace: trace-001",
            "Task: dock",
            "Status: succeeded",
            "- Task dock succeeded.",
            "- Recorded 3 events.",
        )
    )
