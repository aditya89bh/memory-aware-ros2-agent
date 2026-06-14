from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.trace_intelligence import (
    RetryChain,
    RetryChainAnalyzer,
    analyze_retry_chains,
)


def _event(
    event_id: str,
    event_type: EventType,
    timestamp: str,
    retry_group: str | None = None,
) -> MemoryEvent:
    payload = {} if retry_group is None else {"retry_group": retry_group}
    return MemoryEvent(
        event_id=event_id,
        trace_id="trace-001",
        event_type=event_type,
        timestamp=timestamp,
        summary=f"{event_id} summary",
        payload=payload,
    )


def test_analyze_retry_chains_groups_ordered_retry_events() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-2", EventType.TASK_ACTED, "2026-06-14T10:00:02Z", "dock"),
            _event("event-1", EventType.TASK_FAILED, "2026-06-14T10:00:01Z", "dock"),
            _event("event-3", EventType.TASK_OBSERVED, "2026-06-14T10:00:03Z"),
        ),
    )

    assert analyze_retry_chains(trace) == (
        RetryChain("dock", ("event-1", "event-2"), 2, EventType.TASK_ACTED),
    )


def test_analyze_retry_chains_ignores_single_attempt_groups() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_ACTED, "2026-06-14T10:00:01Z", "dock"),
        ),
    )

    assert analyze_retry_chains(trace) == ()


def test_retry_chain_analyzer_returns_serializable_details() -> None:
    trace = TaskTrace(
        "trace-001",
        "dock",
        "2026-06-14T10:00:00Z",
        events=(
            _event("event-1", EventType.TASK_FAILED, "2026-06-14T10:00:01Z", "dock"),
            _event("event-2", EventType.TASK_SUCCEEDED, "2026-06-14T10:00:02Z", "dock"),
        ),
    )

    insight = RetryChainAnalyzer().analyze(trace)

    assert insight.insight_type == "retry_chains"
    assert insight.details["retry_chains"] == (
        {
            "retry_group": "dock",
            "event_ids": ("event-1", "event-2"),
            "attempts": 2,
            "final_event_type": "task.succeeded",
        },
    )
