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
class TaskTrace:
    """Ordered memory events from one robot task workflow."""

    trace_id: str
    task_name: str
    started_at: str
    events: tuple[MemoryEvent, ...] = ()
    ended_at: str | None = None
