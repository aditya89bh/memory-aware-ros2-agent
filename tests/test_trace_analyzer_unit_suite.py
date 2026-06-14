from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    BottleneckAnalyzer,
    EventSequenceAnalyzer,
    ExecutionStatisticsAnalyzer,
    ExperienceSummaryAnalyzer,
    FailurePatternAnalyzer,
    OutcomeSummaryAnalyzer,
    RepeatedFailureAnalyzer,
    RetryChainAnalyzer,
    StateTransitionAnalyzer,
    SuccessPatternAnalyzer,
    TaskDurationAnalyzer,
    TraceAnalyzer,
    TraceAnomalyAnalyzer,
)


def _event(
    event_id: str,
    event_type: EventType,
    second: int,
    payload: dict[str, str] | None = None,
) -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=f"2026-06-14T10:00:0{second}Z",
        summary=f"{event_type.value} summary",
        payload=payload or {},
    )


def test_concrete_trace_analyzers_return_trace_insights() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_STARTED, 1),
            _event("event-2", EventType.TASK_FAILED, 2, {"reason": "timeout"}),
            _event("event-3", EventType.TASK_FAILED, 3, {"reason": "timeout"}),
            _event("event-4", EventType.TASK_SUCCEEDED, 4, {"retry_group": "dock"}),
            _event("event-5", EventType.TASK_SUCCEEDED, 5, {"retry_group": "dock"}),
        ),
        ended_at="2026-06-14T10:00:05Z",
    )
    analyzers: tuple[TraceAnalyzer, ...] = (
        TaskDurationAnalyzer(),
        FailurePatternAnalyzer(),
        SuccessPatternAnalyzer(),
        EventSequenceAnalyzer(),
        RepeatedFailureAnalyzer(),
        TraceAnomalyAnalyzer(require_terminal_event=False),
        RetryChainAnalyzer(),
        StateTransitionAnalyzer(),
        BottleneckAnalyzer(minimum_gap_seconds=1.0),
        OutcomeSummaryAnalyzer(),
        ExecutionStatisticsAnalyzer(),
        ExperienceSummaryAnalyzer(),
    )

    insights = tuple(analyzer.analyze(trace) for analyzer in analyzers)

    assert len(insights) == len(analyzers)
    assert all(insight.trace_id == "trace-001" for insight in insights)
    assert {insight.insight_type for insight in insights} == {
        "bottlenecks",
        "event_sequence",
        "execution_statistics",
        "experience_summary",
        "failure_patterns",
        "outcome_summary",
        "repeated_failures",
        "retry_chains",
        "state_transitions",
        "success_patterns",
        "task_duration",
        "trace_anomalies",
    }
