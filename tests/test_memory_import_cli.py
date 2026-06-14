import json
from pathlib import Path

from memory_aware_ros2_agent.cli import import_memory_bundle


def test_import_memory_bundle_writes_records_by_id(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text(
        json.dumps(
            [
                {
                    "event_id": "event-1",
                    "trace_id": "trace-1",
                    "event_type": "task.observed",
                    "timestamp": "2026-06-14T10:00:00Z",
                    "summary": "Observed part.",
                    "payload": {},
                },
                {
                    "trace_id": "trace-2",
                    "task_name": "demo",
                    "started_at": "2026-06-14T10:00:00Z",
                    "events": [],
                    "ended_at": None,
                },
            ]
        ),
        encoding="utf-8",
    )
    output_dir = tmp_path / "imported"

    written = import_memory_bundle(bundle_path, output_dir)

    assert written == [output_dir / "event-1.json", output_dir / "trace-2.json"]
    assert json.loads(written[0].read_text(encoding="utf-8"))["event_id"] == "event-1"
    assert json.loads(written[1].read_text(encoding="utf-8"))["trace_id"] == "trace-2"
