"""Core memory data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryEvent:
    """A single recorded event from a robot task workflow."""

    event_id: str
    trace_id: str
    event_type: str
    timestamp: str
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class EventMetadata:
    """Context attached to a recorded memory event."""

    source_node_id: str
    created_at: str
    tags: tuple[str, ...] = ()
    priority: int = 0


@dataclass(frozen=True, slots=True)
class TaskTrace:
    """Ordered memory events from one robot task workflow."""

    trace_id: str
    task_name: str
    started_at: str
    events: tuple[MemoryEvent, ...] = ()
    ended_at: str | None = None


@dataclass(frozen=True, slots=True)
class RecallQuery:
    """A request for relevant past memory events."""

    query_id: str
    query_text: str
    requested_at: str
    trace_id: str | None = None
    limit: int = 5
    filters: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class RecallResult:
    """Events returned for a recall query."""

    query_id: str
    events: tuple[MemoryEvent, ...] = ()
    scores: tuple[float, ...] = ()
    generated_at: str | None = None
