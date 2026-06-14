import pytest

from memory_aware_ros2_agent.recall_metrics import (
    RecallMetrics,
    calculate_recall_metrics,
)


def test_calculate_recall_metrics_for_partial_match() -> None:
    metrics = calculate_recall_metrics(
        retrieved_event_ids=("a", "b"),
        relevant_event_ids=("a", "c"),
    )

    assert metrics == RecallMetrics(precision=0.5, recall=0.5, f1=0.5)


def test_calculate_recall_metrics_for_perfect_match() -> None:
    metrics = calculate_recall_metrics(("a", "b"), ("a", "b"))

    assert metrics == RecallMetrics(precision=1.0, recall=1.0, f1=1.0)


def test_calculate_recall_metrics_handles_empty_retrieval() -> None:
    metrics = calculate_recall_metrics((), ("a",))

    assert metrics == RecallMetrics(precision=0.0, recall=0.0, f1=0.0)


def test_calculate_recall_metrics_computes_f1() -> None:
    metrics = calculate_recall_metrics(("a", "b", "c"), ("a", "b"))

    assert metrics.precision == pytest.approx(2 / 3)
    assert metrics.recall == 1.0
    assert metrics.f1 == pytest.approx(0.8)
