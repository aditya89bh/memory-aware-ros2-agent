"""Evaluation reports for recall runs."""

from __future__ import annotations

from dataclasses import dataclass

from memory_aware_ros2_agent.recall_metrics import RecallMetrics


@dataclass(frozen=True)
class RecallEvaluationReport:
    """Aggregate metrics for recall evaluation."""

    case_count: int
    mean_precision: float
    mean_recall: float
    mean_f1: float


def build_recall_evaluation_report(
    metrics: tuple[RecallMetrics, ...],
) -> RecallEvaluationReport:
    """Build an aggregate evaluation report from per-case metrics."""

    if not metrics:
        return RecallEvaluationReport(
            case_count=0,
            mean_precision=0.0,
            mean_recall=0.0,
            mean_f1=0.0,
        )
    case_count = len(metrics)
    return RecallEvaluationReport(
        case_count=case_count,
        mean_precision=sum(metric.precision for metric in metrics) / case_count,
        mean_recall=sum(metric.recall for metric in metrics) / case_count,
        mean_f1=sum(metric.f1 for metric in metrics) / case_count,
    )
