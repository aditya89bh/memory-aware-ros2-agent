"""Core memory data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(str, Enum):
    """Canonical event categories recorded in task memory."""

    TASK_STARTED = "task.started"
    TASK_OBSERVED = "task.observed"
    TASK_DECIDED = "task.decided"
    TASK_ACTED = "task.acted"
    TASK_FAILED = "task.failed"
    TASK_SUCCEEDED = "task.succeeded"


@dataclass(frozen=True, slots=True)
class MemoryEvent:
    """A single recorded event from a robot task workflow."""

    event_id: str
    trace_id: str
    event_type: EventType
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
class SourceNode:
    """Robot or agent node that produced memory data."""

    node_id: str
    node_name: str
    namespace: str = "/"
    capabilities: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class TaskTrace:
    """Ordered memory events from one robot task workflow."""

    trace_id: str
    task_name: str
    started_at: str
    events: tuple[MemoryEvent, ...] = ()
    ended_at: str | None = None


@dataclass(frozen=True, slots=True)
class TaskOutcome:
    """Final outcome summary for a robot task workflow."""

    trace_id: str
    status: str
    completed_at: str
    reason: str | None = None
    metrics: dict[str, Any] = field(default_factory=dict)


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
