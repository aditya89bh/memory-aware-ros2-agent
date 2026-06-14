"""JSON file persistence backend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.models import MemoryEvent, RecallResult, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
    recall_result_from_dict,
    task_trace_from_dict,
)


class JsonFileStore:
    """MemoryStore implementation backed by one JSON document."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({"events": {}, "recall_results": {}, "traces": {}})

    def save_event(self, event: MemoryEvent) -> None:
        """Persist or replace a memory event."""

        data = self._read()
        data["events"][event.event_id] = model_to_dict(event)
        self._write(data)

    def get_event(self, event_id: str) -> MemoryEvent | None:
        """Return a memory event by id, if present."""

        payload = self._read()["events"].get(event_id)
        if payload is None:
            return None
        return memory_event_from_dict(payload)

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        """Return persisted events, optionally filtered by trace id."""

        events = tuple(
            memory_event_from_dict(payload)
            for payload in self._read()["events"].values()
        )
        if trace_id is None:
            return events
        return tuple(event for event in events if event.trace_id == trace_id)

    def save_trace(self, trace: TaskTrace) -> None:
        """Persist or replace a task trace."""

        data = self._read()
        data["traces"][trace.trace_id] = model_to_dict(trace)
        self._write(data)

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        """Return a task trace by id, if present."""

        payload = self._read()["traces"].get(trace_id)
        if payload is None:
            return None
        return task_trace_from_dict(payload)

    def list_traces(self) -> tuple[TaskTrace, ...]:
        """Return persisted task traces."""

        return tuple(
            task_trace_from_dict(payload) for payload in self._read()["traces"].values()
        )

    def save_recall_result(self, result: RecallResult) -> None:
        """Persist or replace a recall result."""

        data = self._read()
        data["recall_results"][result.query_id] = model_to_dict(result)
        self._write(data)

    def get_recall_result(self, query_id: str) -> RecallResult | None:
        """Return a recall result by query id, if present."""

        payload = self._read()["recall_results"].get(query_id)
        if payload is None:
            return None
        return recall_result_from_dict(payload)

    def list_recall_results(self) -> tuple[RecallResult, ...]:
        """Return persisted recall results."""

        return tuple(
            recall_result_from_dict(payload)
            for payload in self._read()["recall_results"].values()
        )

    def close(self) -> None:
        """Release backend resources."""

        return None

    def _read(self) -> dict[str, dict[str, Any]]:
        with self.path.open(encoding="utf-8") as file:
            data = json.load(file)
        return {
            "events": dict(data.get("events", {})),
            "recall_results": dict(data.get("recall_results", {})),
            "traces": dict(data.get("traces", {})),
        }

    def _write(self, data: dict[str, dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, sort_keys=True)
            file.write("\n")
