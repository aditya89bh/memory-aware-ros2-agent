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


@dataclass(frozen=True)
class EventSequenceStep:
    """One ordered step extracted from a trace event."""

    index: int
    event_id: str
    event_type: EventType
    timestamp: str
    summary: str


@dataclass(frozen=True)
class RepeatedFailure:
    """Failure reason that appears multiple times in a trace."""

    reason: str
    count: int


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


def extract_event_sequence(trace: TaskTrace) -> tuple[EventSequenceStep, ...]:
    """Return trace events ordered by timestamp and original position."""

    ordered_events = sorted(
        enumerate(trace.events), key=lambda item: (item[1].timestamp, item[0])
    )
    return tuple(
        EventSequenceStep(
            index=index,
            event_id=event.event_id,
            event_type=event.event_type,
            timestamp=event.timestamp,
            summary=event.summary,
        )
        for index, event in ordered_events
    )


class EventSequenceAnalyzer:
    """Extract an ordered event sequence from a trace."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        sequence = extract_event_sequence(trace)
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="event_sequence",
            summary=f"Trace contains {len(sequence)} ordered events.",
            details={
                "sequence": tuple(
                    {
                        "index": step.index,
                        "event_id": step.event_id,
                        "event_type": step.event_type.value,
                        "timestamp": step.timestamp,
                        "summary": step.summary,
                    }
                    for step in sequence
                )
            },
        )


def detect_repeated_failures(
    trace: TaskTrace, *, minimum_count: int = 2
) -> tuple[RepeatedFailure, ...]:
    """Return failure reasons repeated at least ``minimum_count`` times."""

    return tuple(
        RepeatedFailure(reason=reason, count=count)
        for reason, count in sorted(failure_pattern_counts(trace).items())
        if count >= minimum_count
    )


class RepeatedFailureAnalyzer:
    """Detect repeated failure reasons in a task trace."""

    def __init__(self, *, minimum_count: int = 2) -> None:
        self.minimum_count = minimum_count

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        repeated_failures = detect_repeated_failures(
            trace, minimum_count=self.minimum_count
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="repeated_failures",
            summary=(
                "No repeated failures were detected."
                if not repeated_failures
                else f"Detected {len(repeated_failures)} repeated failure patterns."
            ),
            details={
                "minimum_count": self.minimum_count,
                "repeated_failures": tuple(
                    {"reason": failure.reason, "count": failure.count}
                    for failure in repeated_failures
                ),
            },
        )


def _latest_event_timestamp(trace: TaskTrace) -> str | None:
    if not trace.events:
        return None
    return max(event.timestamp for event in trace.events)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
