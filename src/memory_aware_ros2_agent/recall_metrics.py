"""Metrics for recall evaluation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecallMetrics:
    """Precision/recall/F1 metrics for one recall result."""

    precision: float
    recall: float
    f1: float


def calculate_recall_metrics(
    retrieved_event_ids: tuple[str, ...],
    relevant_event_ids: tuple[str, ...],
) -> RecallMetrics:
    """Calculate precision, recall, and F1 for retrieved event ids."""

    retrieved = set(retrieved_event_ids)
    relevant = set(relevant_event_ids)
    true_positives = len(retrieved & relevant)
    precision = true_positives / len(retrieved) if retrieved else 0.0
    recall = true_positives / len(relevant) if relevant else 0.0
    if precision + recall == 0.0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)
    return RecallMetrics(precision=precision, recall=recall, f1=f1)
