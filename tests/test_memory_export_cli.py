import json
from pathlib import Path

from memory_aware_ros2_agent.cli import export_memory_files


def test_export_memory_files_writes_json_bundle(tmp_path: Path) -> None:
    event_path = tmp_path / "event.json"
    event_path.write_text(
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
    output_path = tmp_path / "bundle.json"

    assert export_memory_files([event_path], output_path) == 1

    assert json.loads(output_path.read_text(encoding="utf-8")) == [
        {
            "event_id": "event-1",
            "trace_id": "trace-1",
            "event_type": "task.observed",
            "timestamp": "2026-06-14T10:00:00Z",
            "summary": "Observed part.",
            "payload": {},
        }
    ]
