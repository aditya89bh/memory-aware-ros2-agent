"""Benchmark datasets for trace intelligence analyzers."""

from __future__ import annotations

from dataclasses import dataclass

from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace


@dataclass(frozen=True)
class TraceAnalyzerBenchmarkCase:
    """One benchmark trace and its expected high-level traits."""

    case_id: str
    trace: TaskTrace
    expected_status: str
    expected_failure_reasons: tuple[str, ...] = ()
    expected_anomaly_types: tuple[str, ...] = ()


@dataclass(frozen=True)
class TraceAnalyzerBenchmarkDataset:
    """Collection of benchmark cases for analyzer evaluation."""

    name: str
    cases: tuple[TraceAnalyzerBenchmarkCase, ...]


def default_trace_analyzer_benchmark_dataset() -> TraceAnalyzerBenchmarkDataset:
    """Return a deterministic benchmark dataset for analyzer tests and reports."""

    return TraceAnalyzerBenchmarkDataset(
        name="default-trace-intelligence",
        cases=(
            TraceAnalyzerBenchmarkCase(
                case_id="successful-dock",
                trace=_trace(
                    trace_id="trace-success",
                    task_name="dock",
                    events=(
                        _event("trace-success", "event-1", EventType.TASK_STARTED, 1),
                        _event("trace-success", "event-2", EventType.TASK_ACTED, 2),
                        _event(
                            "trace-success", "event-3", EventType.TASK_SUCCEEDED, 3
                        ),
                    ),
                    ended_second=3,
                ),
                expected_status="succeeded",
            ),
            TraceAnalyzerBenchmarkCase(
                case_id="repeated-timeout",
                trace=_trace(
                    trace_id="trace-timeout",
                    task_name="navigate",
                    events=(
                        _event(
                            "trace-timeout",
                            "event-1",
                            EventType.TASK_FAILED,
                            1,
                            reason="timeout",
                        ),
                        _event(
                            "trace-timeout",
                            "event-2",
                            EventType.TASK_FAILED,
                            2,
                            reason="timeout",
                        ),
                    ),
                    ended_second=2,
                ),
                expected_status="failed",
                expected_failure_reasons=("timeout",),
            ),
            TraceAnalyzerBenchmarkCase(
                case_id="failure-after-success",
                trace=_trace(
                    trace_id="trace-anomaly",
                    task_name="inspect",
                    events=(
                        _event("trace-anomaly", "event-1", EventType.TASK_SUCCEEDED, 1),
                        _event("trace-anomaly", "event-2", EventType.TASK_FAILED, 2),
                    ),
                    ended_second=2,
                ),
                expected_status="failed",
                expected_anomaly_types=("failure_after_success",),
            ),
        ),
    )


def _trace(
    *,
    trace_id: str,
    task_name: str,
    events: tuple[MemoryEvent, ...],
    ended_second: int,
) -> TaskTrace:
    return TaskTrace(
        trace_id=trace_id,
        task_name=task_name,
        started_at="2026-06-14T10:00:00Z",
        events=events,
        ended_at=f"2026-06-14T10:00:0{ended_second}Z",
    )


def _event(
    trace_id: str,
    event_id: str,
    event_type: EventType,
    second: int,
    *,
    reason: str | None = None,
) -> MemoryEvent:
    payload = {} if reason is None else {"reason": reason}
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=event_type,
        timestamp=f"2026-06-14T10:00:0{second}Z",
        summary=f"{event_type.value} event",
        payload=payload,
    )
