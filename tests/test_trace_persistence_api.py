from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import TaskTrace
from memory_aware_ros2_agent.persistence_api import (
    load_trace,
    load_traces,
    persist_trace,
)


def _trace(trace_id: str) -> TaskTrace:
    return TaskTrace(
        trace_id=trace_id,
        task_name="inspect",
        started_at="2026-06-14T10:00:00Z",
    )


def test_persist_trace_saves_and_returns_trace() -> None:
    store = InMemoryStore()
    trace = _trace("trace-001")

    result = persist_trace(store, trace)

    assert result == trace
    assert load_trace(store, "trace-001") == trace


def test_load_traces_returns_all_persisted_traces() -> None:
    store = InMemoryStore()
    first = _trace("trace-001")
    second = _trace("trace-002")
    persist_trace(store, first)
    persist_trace(store, second)

    assert load_traces(store) == (first, second)
