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
