"""Small benchmark datasets for recall evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallQuery,
    TaskTrace,
)


@dataclass(frozen=True)
class RecallBenchmarkCase:
    """A labeled recall query for benchmark evaluation."""

    query: RecallQuery
    relevant_event_ids: tuple[str, ...]


@dataclass(frozen=True)
class RecallBenchmarkDataset:
    """Events, traces, and labeled queries for recall evaluation."""

    events: tuple[MemoryEvent, ...]
    traces: tuple[TaskTrace, ...]
    cases: tuple[RecallBenchmarkCase, ...]


def small_recall_benchmark_dataset() -> RecallBenchmarkDataset:
    """Return a deterministic recall benchmark dataset."""

    dock_trace = TaskTrace(
        trace_id="trace-dock",
        task_name="dock inspection",
        started_at="2026-06-14T10:00:00Z",
    )
    charge_trace = TaskTrace(
        trace_id="trace-charge",
        task_name="battery charging",
        started_at="2026-06-14T11:00:00Z",
    )
    events = (
        MemoryEvent(
            event_id="event-dock-start",
            trace_id=dock_trace.trace_id,
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T10:00:00Z",
            summary="Robot started dock inspection.",
            payload={"zone": "dock", "source_node_id": "node-dock"},
        ),
        MemoryEvent(
            event_id="event-dock-failed",
            trace_id=dock_trace.trace_id,
            event_type=EventType.TASK_FAILED,
            timestamp="2026-06-14T10:05:00Z",
            summary="Robot failed to inspect blocked dock.",
            payload={"zone": "dock", "source_node_id": "node-dock"},
        ),
        MemoryEvent(
            event_id="event-charge-start",
            trace_id=charge_trace.trace_id,
            event_type=EventType.TASK_STARTED,
            timestamp="2026-06-14T11:00:00Z",
            summary="Robot started battery charging.",
            payload={"zone": "charger", "source_node_id": "node-charge"},
        ),
    )
    cases = (
        RecallBenchmarkCase(
            query=RecallQuery(
                query_id="query-dock",
                query_text="dock",
                requested_at="2026-06-14T12:00:00Z",
            ),
            relevant_event_ids=("event-dock-start", "event-dock-failed"),
        ),
        RecallBenchmarkCase(
            query=RecallQuery(
                query_id="query-failed-dock",
                query_text="dock",
                requested_at="2026-06-14T12:00:00Z",
                filters={"event_types": ("task.failed",)},
            ),
            relevant_event_ids=("event-dock-failed",),
        ),
    )
    return RecallBenchmarkDataset(
        events=events,
        traces=(dock_trace, charge_trace),
        cases=cases,
    )
