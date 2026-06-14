"""Pruning utilities for persistence stores."""

from __future__ import annotations

from dataclasses import dataclass

from memory_aware_ros2_agent.persistence import MemoryStore
from memory_aware_ros2_agent.retention import RetentionPolicy, keep_newest_count


@dataclass(frozen=True)
class PruneResult:
    """Counts of records removed by pruning."""

    events_removed: int = 0
    traces_removed: int = 0
    recall_results_removed: int = 0


def prune_store(store: MemoryStore, policy: RetentionPolicy) -> PruneResult:
    """Apply a retention policy to a store."""

    events_removed = _prune_events(store, policy.max_events)
    traces_removed = _prune_traces(store, policy.max_traces)
    recall_results_removed = _prune_recall_results(
        store,
        policy.max_recall_results,
    )
    return PruneResult(
        events_removed=events_removed,
        traces_removed=traces_removed,
        recall_results_removed=recall_results_removed,
    )


def _prune_events(store: MemoryStore, max_count: int | None) -> int:
    events = sorted(store.list_events(), key=lambda event: event.timestamp)
    prune_count = keep_newest_count(len(events), max_count)
    for event in events[:prune_count]:
        store.delete_event(event.event_id)
    return prune_count


def _prune_traces(store: MemoryStore, max_count: int | None) -> int:
    traces = sorted(store.list_traces(), key=lambda trace: trace.started_at)
    prune_count = keep_newest_count(len(traces), max_count)
    for trace in traces[:prune_count]:
        store.delete_trace(trace.trace_id)
    return prune_count


def _prune_recall_results(store: MemoryStore, max_count: int | None) -> int:
    results = sorted(
        store.list_recall_results(),
        key=lambda result: result.generated_at or "",
    )
    prune_count = keep_newest_count(len(results), max_count)
    for result in results[:prune_count]:
        store.delete_recall_result(result.query_id)
    return prune_count
