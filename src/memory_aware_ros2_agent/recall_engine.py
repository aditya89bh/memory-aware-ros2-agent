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


def filter_events_by_query_time_window(
    events: tuple[MemoryEvent, ...],
    query: RecallQuery,
) -> tuple[MemoryEvent, ...]:
    """Filter events using query.filters['started_at'] and ['ended_at']."""

    started_at = query.filters.get("started_at")
    ended_at = query.filters.get("ended_at")
    if started_at is None and ended_at is None:
        return events
    started = None if started_at is None else str(started_at)
    ended = None if ended_at is None else str(ended_at)
    return tuple(
        event
        for event in events
        if _timestamp_in_window(event.timestamp, started, ended)
    )


class TimeWindowRecallEngine:
    """Recall events whose timestamps fall within a query time window."""

    def recall(self, query: RecallQuery, store: MemoryStore) -> RecallResult:
        """Return persisted events inside a time window."""

        events = filter_events_by_query_time_window(
            store.list_events(query.trace_id),
            query,
        )
        return RecallResult(
            query_id=query.query_id,
            events=events[: query.limit],
            scores=tuple(1.0 for _event in events[: query.limit]),
        )


def _timestamp_in_window(
    timestamp: str,
    started_at: str | None,
    ended_at: str | None,
) -> bool:
    if started_at is not None and timestamp < started_at:
        return False
    return not (ended_at is not None and timestamp > ended_at)


def recency_scores(events: tuple[MemoryEvent, ...]) -> tuple[float, ...]:
    """Score events by timestamp recency in the range 0.0 to 1.0."""

    if not events:
        return ()
    if len(events) == 1:
        return (1.0,)
    ordered_timestamps = sorted({event.timestamp for event in events})
    if len(ordered_timestamps) == 1:
        return tuple(1.0 for _event in events)
    max_index = len(ordered_timestamps) - 1
    timestamp_scores = {
        timestamp: index / max_index
        for index, timestamp in enumerate(ordered_timestamps)
    }
    return tuple(timestamp_scores[event.timestamp] for event in events)


def frequency_scores(events: tuple[MemoryEvent, ...]) -> tuple[float, ...]:
    """Score events by trace frequency in the range 0.0 to 1.0."""

    if not events:
        return ()
    trace_counts: dict[str, int] = {}
    for event in events:
        trace_counts[event.trace_id] = trace_counts.get(event.trace_id, 0) + 1
    max_count = max(trace_counts.values())
    return tuple(trace_counts[event.trace_id] / max_count for event in events)


def rank_events_by_score(
    events: tuple[MemoryEvent, ...],
    scores: tuple[float, ...],
) -> tuple[MemoryEvent, ...]:
    """Return events sorted by descending score while preserving stable ties."""

    if len(events) != len(scores):
        msg = "events and scores must have the same length"
        raise ValueError(msg)
    ranked = sorted(
        enumerate(zip(events, scores, strict=True)),
        key=lambda item: (-item[1][1], item[0]),
    )
    return tuple(event for _index, (event, _score) in ranked)


def composite_scores(
    score_vectors: tuple[tuple[float, ...], ...],
    weights: tuple[float, ...],
) -> tuple[float, ...]:
    """Combine score vectors with normalized weights."""

    if len(score_vectors) != len(weights):
        msg = "score_vectors and weights must have the same length"
        raise ValueError(msg)
    if not score_vectors:
        return ()
    expected_length = len(score_vectors[0])
    if any(len(vector) != expected_length for vector in score_vectors):
        msg = "score vectors must have the same length"
        raise ValueError(msg)
    total_weight = sum(weights)
    if total_weight <= 0:
        msg = "weights must sum to a positive value"
        raise ValueError(msg)
    return tuple(
        sum(
            vector[index] * weight
            for vector, weight in zip(score_vectors, weights, strict=True)
        )
        / total_weight
        for index in range(expected_length)
    )


def filter_events_by_query_metadata(
    events: tuple[MemoryEvent, ...],
    query: RecallQuery,
) -> tuple[MemoryEvent, ...]:
    """Filter events using exact payload matches from query.filters['metadata']."""

    metadata = query.filters.get("metadata")
    if metadata is None:
        return events
    if not isinstance(metadata, dict):
        msg = "metadata filter must be a mapping"
        raise ValueError(msg)
    return tuple(
        event
        for event in events
        if all(event.payload.get(str(key)) == value for key, value in metadata.items())
    )


def filter_events_by_query_source_nodes(
    events: tuple[MemoryEvent, ...],
    query: RecallQuery,
) -> tuple[MemoryEvent, ...]:
    """Filter events by payload source_node_id values."""

    source_node_ids = query.filters.get("source_node_ids")
    if source_node_ids is None:
        return events
    if isinstance(source_node_ids, str):
        allowed = {source_node_ids}
    else:
        allowed = {str(source_node_id) for source_node_id in source_node_ids}
    return tuple(
        event
        for event in events
        if str(event.payload.get("source_node_id", "")) in allowed
    )


def top_k_events(
    events: tuple[MemoryEvent, ...],
    scores: tuple[float, ...],
    k: int,
) -> tuple[MemoryEvent, ...]:
    """Return the top-k events by score."""

    if k <= 0:
        return ()
    return rank_events_by_score(events, scores)[:k]


def paginate_events(
    events: tuple[MemoryEvent, ...],
    query: RecallQuery,
) -> tuple[MemoryEvent, ...]:
    """Paginate events using query filters offset and page_size."""

    offset = max(0, int(query.filters.get("offset", 0)))
    page_size = int(query.filters.get("page_size", query.limit))
    if page_size <= 0:
        return ()
    return events[offset : offset + page_size]
