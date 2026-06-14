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


@dataclass(frozen=True)
class TraceAnomaly:
    """Unusual condition detected in a trace."""

    anomaly_type: str
    severity: str
    description: str


@dataclass(frozen=True)
class RetryChain:
    """Retry attempts that belong to the same logical operation."""

    retry_group: str
    event_ids: tuple[str, ...]
    attempts: int
    final_event_type: EventType


@dataclass(frozen=True)
class StateTransition:
    """Adjacent transition between event types in a trace."""

    from_event_type: EventType
    to_event_type: EventType
    count: int


@dataclass(frozen=True)
class TraceBottleneck:
    """Long delay between adjacent trace events."""

    from_event_id: str
    to_event_id: str
    duration_seconds: float


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


def detect_trace_anomalies(
    trace: TaskTrace,
    *,
    max_duration_seconds: float | None = None,
    require_terminal_event: bool = True,
) -> tuple[TraceAnomaly, ...]:
    """Detect deterministic anomalies in a task trace."""

    anomalies: list[TraceAnomaly] = []
    sequence = extract_event_sequence(trace)
    terminal_types = {EventType.TASK_FAILED, EventType.TASK_SUCCEEDED}

    if require_terminal_event and not any(
        step.event_type in terminal_types for step in sequence
    ):
        anomalies.append(
            TraceAnomaly(
                anomaly_type="missing_terminal_event",
                severity="medium",
                description="Trace has no success or failure terminal event.",
            )
        )

    duration = task_duration_seconds(trace)
    if (
        max_duration_seconds is not None
        and duration is not None
        and duration > max_duration_seconds
    ):
        anomalies.append(
            TraceAnomaly(
                anomaly_type="duration_exceeded",
                severity="high",
                description=(
                    f"Trace duration {duration:.1f}s exceeded "
                    f"{max_duration_seconds:.1f}s."
                ),
            )
        )

    seen_success = False
    for step in sequence:
        if step.event_type == EventType.TASK_SUCCEEDED:
            seen_success = True
        if seen_success and step.event_type == EventType.TASK_FAILED:
            anomalies.append(
                TraceAnomaly(
                    anomaly_type="failure_after_success",
                    severity="high",
                    description="Failure event appeared after a success event.",
                )
            )
            break

    return tuple(anomalies)


class TraceAnomalyAnalyzer:
    """Analyze a trace for deterministic anomalies."""

    def __init__(
        self,
        *,
        max_duration_seconds: float | None = None,
        require_terminal_event: bool = True,
    ) -> None:
        self.max_duration_seconds = max_duration_seconds
        self.require_terminal_event = require_terminal_event

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        anomalies = detect_trace_anomalies(
            trace,
            max_duration_seconds=self.max_duration_seconds,
            require_terminal_event=self.require_terminal_event,
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="trace_anomalies",
            summary=(
                "No trace anomalies were detected."
                if not anomalies
                else f"Detected {len(anomalies)} trace anomalies."
            ),
            details={
                "anomalies": tuple(
                    {
                        "anomaly_type": anomaly.anomaly_type,
                        "severity": anomaly.severity,
                        "description": anomaly.description,
                    }
                    for anomaly in anomalies
                )
            },
        )


def analyze_retry_chains(trace: TaskTrace) -> tuple[RetryChain, ...]:
    """Group retry events by their ``retry_group`` payload value."""

    grouped_events: dict[str, list[MemoryEvent]] = {}
    for step in extract_event_sequence(trace):
        event = trace.events[step.index]
        retry_group = event.payload.get("retry_group")
        if retry_group is None:
            continue
        grouped_events.setdefault(str(retry_group), []).append(event)

    chains: list[RetryChain] = []
    for retry_group, events in sorted(grouped_events.items()):
        if len(events) < 2:
            continue
        chains.append(
            RetryChain(
                retry_group=retry_group,
                event_ids=tuple(event.event_id for event in events),
                attempts=len(events),
                final_event_type=events[-1].event_type,
            )
        )
    return tuple(chains)


class RetryChainAnalyzer:
    """Analyze retry chains in a task trace."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        chains = analyze_retry_chains(trace)
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="retry_chains",
            summary=(
                "No retry chains were detected."
                if not chains
                else f"Detected {len(chains)} retry chains."
            ),
            details={
                "retry_chains": tuple(
                    {
                        "retry_group": chain.retry_group,
                        "event_ids": chain.event_ids,
                        "attempts": chain.attempts,
                        "final_event_type": chain.final_event_type.value,
                    }
                    for chain in chains
                )
            },
        )


def analyze_state_transitions(trace: TaskTrace) -> tuple[StateTransition, ...]:
    """Count adjacent event-type transitions in timestamp order."""

    sequence = extract_event_sequence(trace)
    counts: dict[tuple[EventType, EventType], int] = {}
    for current_step, next_step in zip(sequence, sequence[1:], strict=False):
        key = (current_step.event_type, next_step.event_type)
        counts[key] = counts.get(key, 0) + 1
    return tuple(
        StateTransition(
            from_event_type=from_event_type,
            to_event_type=to_event_type,
            count=count,
        )
        for (from_event_type, to_event_type), count in sorted(
            counts.items(), key=lambda item: (item[0][0].value, item[0][1].value)
        )
    )


class StateTransitionAnalyzer:
    """Analyze event-type transitions in a task trace."""

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        transitions = analyze_state_transitions(trace)
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="state_transitions",
            summary=f"Detected {len(transitions)} distinct state transitions.",
            details={
                "transitions": tuple(
                    {
                        "from_event_type": transition.from_event_type.value,
                        "to_event_type": transition.to_event_type.value,
                        "count": transition.count,
                    }
                    for transition in transitions
                )
            },
        )


def identify_bottlenecks(
    trace: TaskTrace, *, minimum_gap_seconds: float
) -> tuple[TraceBottleneck, ...]:
    """Return adjacent event gaps at or above ``minimum_gap_seconds``."""

    sequence = extract_event_sequence(trace)
    bottlenecks: list[TraceBottleneck] = []
    for current_step, next_step in zip(sequence, sequence[1:], strict=False):
        gap_seconds = (
            _parse_timestamp(next_step.timestamp)
            - _parse_timestamp(current_step.timestamp)
        ).total_seconds()
        if gap_seconds >= minimum_gap_seconds:
            bottlenecks.append(
                TraceBottleneck(
                    from_event_id=current_step.event_id,
                    to_event_id=next_step.event_id,
                    duration_seconds=gap_seconds,
                )
            )
    return tuple(bottlenecks)


class BottleneckAnalyzer:
    """Analyze long gaps between adjacent trace events."""

    def __init__(self, *, minimum_gap_seconds: float) -> None:
        self.minimum_gap_seconds = minimum_gap_seconds

    def analyze(self, trace: TaskTrace) -> TraceInsight:
        bottlenecks = identify_bottlenecks(
            trace, minimum_gap_seconds=self.minimum_gap_seconds
        )
        return TraceInsight(
            trace_id=trace.trace_id,
            insight_type="bottlenecks",
            summary=(
                "No bottlenecks were detected."
                if not bottlenecks
                else f"Detected {len(bottlenecks)} bottlenecks."
            ),
            details={
                "minimum_gap_seconds": self.minimum_gap_seconds,
                "bottlenecks": tuple(
                    {
                        "from_event_id": bottleneck.from_event_id,
                        "to_event_id": bottleneck.to_event_id,
                        "duration_seconds": bottleneck.duration_seconds,
                    }
                    for bottleneck in bottlenecks
                ),
            },
        )


def _latest_event_timestamp(trace: TaskTrace) -> str | None:
    if not trace.events:
        return None
    return max(event.timestamp for event in trace.events)


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
