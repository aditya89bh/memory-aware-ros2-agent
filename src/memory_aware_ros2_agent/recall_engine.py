"""Recall engine interfaces and helpers."""

from __future__ import annotations

from typing import Protocol

from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallQuery,
    RecallResult,
)
from memory_aware_ros2_agent.persistence import MemoryStore


class RecallEngine(Protocol):
    """Contract for retrieving relevant memories from persisted experience."""

    def recall(self, query: RecallQuery, store: MemoryStore) -> RecallResult:
        """Return relevant persisted memories for a query."""


class ExactMatchRecallEngine:
    """Recall events whose text contains the query text."""

    def recall(self, query: RecallQuery, store: MemoryStore) -> RecallResult:
        """Return events with exact case-insensitive text matches."""

        query_text = query.query_text.casefold().strip()
        if not query_text:
            return RecallResult(query_id=query.query_id)
        events = tuple(
            event
            for event in store.list_events(query.trace_id)
            if query_text in _event_search_text(event)
        )
        return RecallResult(
            query_id=query.query_id,
            events=events[: query.limit],
            scores=tuple(1.0 for _event in events[: query.limit]),
        )


def _event_search_text(event: MemoryEvent) -> str:
    payload_text = " ".join(f"{key} {value}" for key, value in event.payload.items())
    return f"{event.summary} {payload_text}".casefold()


class TaskBasedRecallEngine:
    """Recall events from traces whose task name matches the query text."""

    def recall(self, query: RecallQuery, store: MemoryStore) -> RecallResult:
        """Return events from matching persisted task traces."""

        query_text = query.query_text.casefold().strip()
        if not query_text:
            return RecallResult(query_id=query.query_id)
        matching_trace_ids = {
            trace.trace_id
            for trace in store.list_traces()
            if query_text in trace.task_name.casefold()
        }
        events = tuple(
            event
            for event in store.list_events()
            if event.trace_id in matching_trace_ids
        )
        return RecallResult(
            query_id=query.query_id,
            events=events[: query.limit],
            scores=tuple(1.0 for _event in events[: query.limit]),
        )


def filter_events_by_query_event_types(
    events: tuple[MemoryEvent, ...],
    query: RecallQuery,
) -> tuple[MemoryEvent, ...]:
    """Filter events using query.filters['event_types'] when present."""

    allowed_types = event_types_from_query(query)
    if not allowed_types:
        return events
    return tuple(event for event in events if event.event_type in allowed_types)


def event_types_from_query(query: RecallQuery) -> tuple[EventType, ...]:
    """Read event type filters from a recall query."""

    raw_event_types = query.filters.get("event_types")
    if raw_event_types is None:
        return ()
    if isinstance(raw_event_types, str):
        raw_values = (raw_event_types,)
    else:
        raw_values = tuple(raw_event_types)
    return tuple(EventType(str(value)) for value in raw_values)
