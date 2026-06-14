"""Trace intelligence interfaces and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
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


def task_duration_seconds(trace: TaskTrace) -> float | None:
    """Return trace duration in seconds when timestamps are available."""

    end_timestamp = trace.ended_at or _latest_event_timestamp(trace)
    if end_timestamp is None:
        return None
    return (
        _parse_timestamp(end_timestamp) - _parse_timestamp(trace.started_at)
    ).total_seconds()


class TaskDurationAnalyzer:
    """Analyze how long a task trace took."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        duration = task_duration_seconds(trace)
        summary = (
            "Task duration is unknown."
            if duration is None
            else f"Task ran for {duration:.1f} seconds."
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="task_duration",
            summary=summary,
            details={"duration_seconds": duration},
        )


def _latest_event_timestamp(trace: TaskTrace) -> str | None:
    if not trace.events:
        return None
    return max(event.timestamp for event in trace.events)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
