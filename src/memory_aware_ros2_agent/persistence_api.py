"""High-level persistence APIs."""

from __future__ import annotations

from memory_aware_ros2_agent.models import MemoryEvent, RecallResult, TaskTrace
from memory_aware_ros2_agent.persistence import MemoryStore


def persist_event(store: MemoryStore, event: MemoryEvent) -> MemoryEvent:
    """Persist a memory event and return it for caller chaining."""

    store.save_event(event)
    return event


def load_event(store: MemoryStore, event_id: str) -> MemoryEvent | None:
    """Load a memory event by id."""

    return store.get_event(event_id)


def load_events_for_trace(
    store: MemoryStore,
    trace_id: str,
) -> tuple[MemoryEvent, ...]:
    """Load memory events belonging to a trace."""

    return store.list_events(trace_id)


def persist_trace(store: MemoryStore, trace: TaskTrace) -> TaskTrace:
    """Persist a task trace and return it for caller chaining."""

    store.save_trace(trace)
    return trace


def load_trace(store: MemoryStore, trace_id: str) -> TaskTrace | None:
    """Load a task trace by id."""

    return store.get_trace(trace_id)


def load_traces(store: MemoryStore) -> tuple[TaskTrace, ...]:
    """Load all task traces from a store."""

    return store.list_traces()


def persist_recall_result(
    store: MemoryStore,
    result: RecallResult,
) -> RecallResult:
    """Persist a recall result and return it for caller chaining."""

    store.save_recall_result(result)
    return result


def load_recall_result(store: MemoryStore, query_id: str) -> RecallResult | None:
    """Load a recall result by query id."""

    return store.get_recall_result(query_id)


def load_recall_results(store: MemoryStore) -> tuple[RecallResult, ...]:
    """Load all recall results from a store."""

    return store.list_recall_results()
