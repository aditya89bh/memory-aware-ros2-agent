from memory_aware_ros2_agent.recall_metrics import RecallMetrics
from memory_aware_ros2_agent.recall_reports import (
    RecallEvaluationReport,
    build_recall_evaluation_report,
)


def test_build_recall_evaluation_report_averages_metrics() -> None:
    report = build_recall_evaluation_report(
        (
            RecallMetrics(precision=1.0, recall=0.5, f1=0.66),
            RecallMetrics(precision=0.5, recall=1.0, f1=0.66),
        )
    )

    assert report == RecallEvaluationReport(
        case_count=2,
        mean_precision=0.75,
        mean_recall=0.75,
        mean_f1=0.66,
    )


def test_build_recall_evaluation_report_handles_empty_metrics() -> None:
    assert build_recall_evaluation_report(()) == RecallEvaluationReport(
        case_count=0,
        mean_precision=0.0,
        mean_recall=0.0,
        mean_f1=0.0,
    )
