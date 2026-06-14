from memory_aware_ros2_agent.recall_reports import RecallEvaluationReport
from memory_aware_ros2_agent.recall_visualizations import (
    render_metric_bar,
    render_recall_report,
)


def test_render_metric_bar_clamps_and_formats_metric() -> None:
    assert render_metric_bar("precision", 0.5, width=4) == "precision: [##--] 0.50"
    assert render_metric_bar("precision", 2.0, width=4) == "precision: [####] 1.00"


def test_render_recall_report_includes_all_metrics() -> None:
    report = RecallEvaluationReport(
        case_count=2,
        mean_precision=0.75,
        mean_recall=0.5,
        mean_f1=0.6,
    )

    rendered = render_recall_report(report)

    assert "cases: 2" in rendered
    assert "precision:" in rendered
    assert "recall:" in rendered
    assert "f1:" in rendered
