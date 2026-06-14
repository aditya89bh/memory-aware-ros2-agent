import json
from pathlib import Path

from memory_aware_ros2_agent.json_file_store import JsonFileStore
from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace
from memory_aware_ros2_agent.persistence import MemoryStore


def _event(event_id: str, trace_id: str = "trace-001") -> MemoryEvent:
    return MemoryEvent(
        event_id=event_id,
        trace_id=trace_id,
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-14T10:00:00Z",
        summary="Task started.",
    )


def test_json_file_store_creates_storage_file(tmp_path: Path) -> None:
    path = tmp_path / "memory.json"

    JsonFileStore(path)

    assert json.loads(path.read_text(encoding="utf-8")) == {
        "events": {},
        "traces": {},
    }


def test_json_file_store_round_trips_events_and_traces(tmp_path: Path) -> None:
    store: MemoryStore = JsonFileStore(tmp_path / "memory.json")
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


def test_json_file_store_reloads_existing_data(tmp_path: Path) -> None:
    path = tmp_path / "memory.json"
    first_store = JsonFileStore(path)
    event = _event("event-001")
    first_store.save_event(event)

    second_store = JsonFileStore(path)

    assert second_store.get_event("event-001") == event
