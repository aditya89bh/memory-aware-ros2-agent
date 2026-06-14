"""Developer CLI utilities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.performance_benchmarks import (
    benchmark_exact_match_recall,
    benchmark_load_fixture_creation,
)
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
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


def import_memory_bundle(bundle_path: Path, output_dir: Path) -> list[Path]:
    """Import a JSON bundle into one file per memory record."""

    records = _load_json(bundle_path)
    if not isinstance(records, list):
        raise ValueError("memory bundle must contain a JSON array")
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError("memory bundle records must be JSON objects")
        record_id = str(record.get("event_id") or record.get("trace_id") or index)
        path = output_dir / f"{record_id}.json"
        path.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        written.append(path)
    return written


def import_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Import a memory JSON bundle.")
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    paths = import_memory_bundle(args.bundle, args.output_dir)
    print(f"imported {len(paths)} memory records into {args.output_dir}")


def run_benchmarks(event_count: int, limit: int) -> list[dict[str, Any]]:
    """Run deterministic development benchmarks."""

    results = [
        benchmark_load_fixture_creation(event_count),
        benchmark_exact_match_recall(event_count, limit),
    ]
    return [model_to_dict(result) for result in results]


def benchmark_main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run memory agent benchmarks.")
    parser.add_argument("--event-count", default=100, type=int)
    parser.add_argument("--limit", default=5, type=int)
    args = parser.parse_args(argv)
    print(json.dumps(run_benchmarks(args.event_count, args.limit), indent=2))
