from pathlib import Path

from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.persistence import MemoryStore
from memory_aware_ros2_agent.sqlite_store import SQLiteStore, sqlite_tables


def _event(event_id: str, trace_id: str = "trace-001") -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )


def test_sqlite_store_initializes_schema(tmp_path: Path) -> None:
    store = SQLiteStore(tmp_path / "memory.db")

    assert sqlite_tables(store) == ("memory_events", "task_traces")


def test_sqlite_store_round_trips_events_and_traces(tmp_path: Path) -> None:
    store: MemoryStore = SQLiteStore(tmp_path / "memory.db")
    event = _event("event-001")
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="inspect",
        started_at="2026-06-14T10:00:00Z",
        events=(event,),
    )

    store.save_event(event)
    store.save_trace(trace)

    assert store.get_event("event-001") == event
    assert store.get_trace("trace-001") == trace
    assert store.list_events("trace-001") == (event,)
    assert store.list_traces() == (trace,)


def test_sqlite_store_reopens_existing_database(tmp_path: Path) -> None:
    path = tmp_path / "memory.db"
    first_store = SQLiteStore(path)
    event = _event("event-001")
    first_store.save_event(event)
    first_store.close()

    second_store = SQLiteStore(path)

    assert second_store.get_event("event-001") == event
