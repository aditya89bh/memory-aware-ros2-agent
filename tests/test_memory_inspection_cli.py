import json
from pathlib import Path

from memory_aware_ros2_agent.cli import inspect_memory_file


def test_inspect_memory_file_summarizes_event(tmp_path: Path) -> None:
    path = tmp_path / "event.json"
    path.write_text(
        json.dumps(
            {
                "event_id": "event-1",
                "trace_id": "trace-1",
                "event_type": "task.observed",
                "timestamp": "2026-06-14T10:00:00Z",
                "summary": "Observed part.",
                "payload": {},
            }
        ),
        encoding="utf-8",
    )

    assert inspect_memory_file(path) == "event event-1 [task.observed] Observed part."


def test_inspect_memory_file_summarizes_trace(tmp_path: Path) -> None:
    path = tmp_path / "trace.json"
    path.write_text(
        json.dumps(
            {
                "trace_id": "trace-1",
                "task_name": "demo",
                "started_at": "2026-06-14T10:00:00Z",
                "events": [],
                "ended_at": None,
            }
        ),
        encoding="utf-8",
    )

    assert inspect_memory_file(path) == "trace trace-1 task=demo events=0"
