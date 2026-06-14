"""Trace intelligence interfaces and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from memory_aware_ros2_agent.models import TaskTrace


@dataclass(frozen=True)
class TraceInsight:
    """Structured insight produced from a task trace."""

    trace_id: str
    insight_type: str
    summary: str
    details: dict[str, Any] = field(default_factory=dict)


class TraceAnalyzer(Protocol):
    """Contract for turning raw task traces into actionable insight."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        """Analyze one task trace."""
