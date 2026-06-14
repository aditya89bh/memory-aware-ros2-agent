"""High-level persistence APIs."""

from __future__ import annotations

from memory_aware_ros2_agent.models import MemoryEvent
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
