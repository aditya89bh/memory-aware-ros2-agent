"""In-memory persistence backend."""

from __future__ import annotations

from memory_aware_ros2_agent.models import MemoryEvent, RecallResult, TaskTrace


class InMemoryStore:
    """MemoryStore implementation backed by local dictionaries."""

    def __init__(self) -> None:
        self._events: dict[str, MemoryEvent] = {}
        self._traces: dict[str, TaskTrace] = {}
        self._recall_results: dict[str, RecallResult] = {}

    def save_event(self, event: MemoryEvent) -> None:
        """Persist or replace a memory event."""

        self._events[event.event_id] = event

    def get_event(self, event_id: str) -> MemoryEvent | None:
        """Return a memory event by id, if present."""

        return self._events.get(event_id)

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        """Return persisted events, optionally filtered by trace id."""

        events = tuple(self._events.values())
        if trace_id is None:
            return events
        return tuple(event for event in events if event.trace_id == trace_id)

    def save_trace(self, trace: TaskTrace) -> None:
        """Persist or replace a task trace."""

        self._traces[trace.trace_id] = trace

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        """Return a task trace by id, if present."""

        return self._traces.get(trace_id)

    def list_traces(self) -> tuple[TaskTrace, ...]:
        """Return persisted task traces."""

        return tuple(self._traces.values())

    def save_recall_result(self, result: RecallResult) -> None:
        """Persist or replace a recall result."""

        self._recall_results[result.query_id] = result

    def get_recall_result(self, query_id: str) -> RecallResult | None:
        """Return a recall result by query id, if present."""

        return self._recall_results.get(query_id)

    def list_recall_results(self) -> tuple[RecallResult, ...]:
        """Return persisted recall results."""

        return tuple(self._recall_results.values())

    def close(self) -> None:
        """Release backend resources."""

        return None
