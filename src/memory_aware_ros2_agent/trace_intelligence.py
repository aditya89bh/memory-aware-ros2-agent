"""Trace intelligence interfaces and helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol

from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace


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


def failure_events(trace: TaskTrace) -> tuple[MemoryEvent, ...]:
    """Return failure events from a trace."""

    return tuple(
        event for event in trace.events if event.event_type == EventType.TASK_FAILED
    )


def failure_pattern_counts(trace: TaskTrace) -> dict[str, int]:
    """Count failure reasons from event payloads and summaries."""

    counts: dict[str, int] = {}
    for event in failure_events(trace):
        reason = str(event.payload.get("reason") or event.summary)
        counts[reason] = counts.get(reason, 0) + 1
    return counts


class FailurePatternAnalyzer:
    """Analyze failure patterns in a task trace."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        counts = failure_pattern_counts(trace)
        if not counts:
            return TraceInsight(
                trace_id=trace.trace_id,
                insight_type="failure_patterns",
                summary="No failures were recorded.",
                details={"failure_count": 0, "patterns": {}},
            )

        dominant_reason, dominant_count = max(
            counts.items(), key=lambda item: (item[1], item[0])
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="failure_patterns",
            summary=(
                f"Most common failure was '{dominant_reason}' "
                f"({dominant_count} occurrences)."
            ),
            details={"failure_count": sum(counts.values()), "patterns": counts},
        )


def success_events(trace: TaskTrace) -> tuple[MemoryEvent, ...]:
    """Return success events from a trace."""

    return tuple(
        event for event in trace.events if event.event_type == EventType.TASK_SUCCEEDED
    )


def success_pattern_counts(trace: TaskTrace) -> dict[str, int]:
    """Count success signals from event payloads and summaries."""

    counts: dict[str, int] = {}
    for event in success_events(trace):
        signal = str(
            event.payload.get("signal") or event.payload.get("reason") or event.summary
        )
        counts[signal] = counts.get(signal, 0) + 1
    return counts


class SuccessPatternAnalyzer:
    """Analyze success patterns in a task trace."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        counts = success_pattern_counts(trace)
        if not counts:
            return TraceInsight(
                trace_id=trace.trace_id,
                insight_type="success_patterns",
                summary="No success events were recorded.",
                details={"success_count": 0, "patterns": {}},
            )

        dominant_signal, dominant_count = max(
            counts.items(), key=lambda item: (item[1], item[0])
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="success_patterns",
            summary=(
                f"Most common success signal was '{dominant_signal}' "
                f"({dominant_count} occurrences)."
            ),
            details={"success_count": sum(counts.values()), "patterns": counts},
        )


def _latest_event_timestamp(trace: TaskTrace) -> str | None:
    if not trace.events:
        return None
    return max(event.timestamp for event in trace.events)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
