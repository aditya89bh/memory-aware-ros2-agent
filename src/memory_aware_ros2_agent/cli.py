"""Developer CLI utilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    task_trace_from_dict,
)


def inspect_memory_file(path: Path) -> str:
    """Return a human-readable summary for a memory JSON file."""

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("memory file must contain a JSON object")
    if "event_id" in data:
        event = memory_event_from_dict(data)
        return f"event {event.event_id} [{event.event_type.value}] {event.summary}"
    if "trace_id" in data and "events" in data:
        trace = task_trace_from_dict(data)
        return (
            f"trace {trace.trace_id} "
            f"task={trace.task_name} events={len(trace.events)}"
        )
    raise ValueError("unsupported memory file shape")


def inspect_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Inspect a memory JSON file.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    print(inspect_memory_file(args.path))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def export_memory_files(paths: list[Path], output_path: Path) -> int:
    """Export memory JSON files into a single JSON bundle."""

    bundle = [_load_json(path) for path in paths]
    output_path.write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return len(bundle)


def export_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export memory JSON files.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    count = export_memory_files(args.paths, args.output)
    print(f"exported {count} memory records to {args.output}")
