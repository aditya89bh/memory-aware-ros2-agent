import json
from pathlib import Path

from memory_aware_ros2_agent.event_log_store import EventLogStore
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


def test_event_log_store_appends_event_records(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    store = EventLogStore(path)
    event = _event("event-001")

    store.save_event(event)

    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert records[0]["record_type"] == "memory_event"
    assert records[0]["payload"]["event_id"] == "event-001"


def test_event_log_store_replays_existing_events(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    first_store = EventLogStore(path)
    event = _event("event-001")
    first_store.save_event(event)

    second_store = EventLogStore(path)

    assert second_store.get_event("event-001") == event


def test_event_log_store_filters_events_by_trace_id(tmp_path: Path) -> None:
    store = EventLogStore(tmp_path / "events.jsonl")
    first = _event("event-001", "trace-001")
    second = _event("event-002", "trace-002")

    store.save_event(first)
    store.save_event(second)

    assert store.list_events("trace-001") == (first,)


def test_event_log_store_satisfies_memory_store_protocol(tmp_path: Path) -> None:
    store: MemoryStore = EventLogStore(tmp_path / "events.jsonl")
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="inspect",
        started_at="2026-06-14T10:00:00Z",
    )

    store.save_trace(trace)

    assert store.get_trace("trace-001") == trace
