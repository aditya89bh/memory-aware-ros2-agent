from collections.abc import Callable
from pathlib import Path

import pytest

from memory_aware_ros2_agent.event_log_store import EventLogStore
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.json_file_store import JsonFileStore
from memory_aware_ros2_agent.models import (
    EventType,
    MemoryEvent,
    RecallResult,
    TaskTrace,
)
from memory_aware_ros2_agent.persistence import MemoryStore
from memory_aware_ros2_agent.sqlite_store import SQLiteStore

StoreFactory = Callable[[Path], MemoryStore]


def _event() -> MemoryEvent:
    return MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )


@pytest.mark.parametrize(
    "factory",
    [
        lambda _tmp_path: InMemoryStore(),
        lambda tmp_path: JsonFileStore(tmp_path / "memory.json"),
        lambda tmp_path: SQLiteStore(tmp_path / "memory.db"),
        lambda tmp_path: EventLogStore(tmp_path / "events.jsonl"),
    ],
)
def test_backends_share_event_and_recall_contract(
    tmp_path: Path,
    factory: StoreFactory,
) -> None:
    store = factory(tmp_path)
    event = _event()
    result = RecallResult(query_id="query-001", generated_at="2026-06-14T10:01:00Z")

    store.save_event(event)
    store.save_recall_result(result)

    assert store.get_event(event.event_id) == event
    assert store.list_events(event.trace_id) == (event,)
    assert store.get_recall_result(result.query_id) == result

    store.delete_event(event.event_id)
    store.delete_recall_result(result.query_id)

    assert store.get_event(event.event_id) is None
    assert store.get_recall_result(result.query_id) is None


@pytest.mark.parametrize(
    "factory",
    [
        lambda _tmp_path: InMemoryStore(),
        lambda tmp_path: JsonFileStore(tmp_path / "memory.json"),
        lambda tmp_path: SQLiteStore(tmp_path / "memory.db"),
    ],
)
def test_backends_share_trace_contract(
    tmp_path: Path,
    factory: StoreFactory,
) -> None:
    store = factory(tmp_path)
    trace = TaskTrace("trace-001", "inspect", "2026-06-14T10:00:00Z")

    store.save_trace(trace)

    assert store.get_trace(trace.trace_id) == trace
    assert store.list_traces() == (trace,)

    store.delete_trace(trace.trace_id)

    assert store.get_trace(trace.trace_id) is None
