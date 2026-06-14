"""Text visualizations for recall evaluation."""

from __future__ import annotations

from memory_aware_ros2_agent.recall_reports import RecallEvaluationReport


def render_metric_bar(label: str, value: float, width: int = 20) -> str:
    """Render one metric as an ASCII bar."""

    clamped = min(1.0, max(0.0, value))
    filled = round(clamped * width)
    bar = "#" * filled + "-" * (width - filled)
    return f"{label}: [{bar}] {clamped:.2f}"


def render_recall_report(report: RecallEvaluationReport) -> str:
    """Render a recall evaluation report as text."""

    lines = [
        f"cases: {report.case_count}",
        render_metric_bar("precision", report.mean_precision),
        render_metric_bar("recall", report.mean_recall),
        render_metric_bar("f1", report.mean_f1),
    ]
    return "\n".join(lines)
