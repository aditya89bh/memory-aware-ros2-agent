"""Append-only event log persistence backend."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import MemoryEvent, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
)


class EventLogStore:
    """Append-only JSONL backend for memory events."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)
        self._store = InMemoryStore()
        self._replay()

    def save_event(self, event: MemoryEvent) -> None:
        """Append and persist a memory event."""

        self._append({"record_type": "memory_event", "payload": model_to_dict(event)})
        self._store.save_event(event)

    def get_event(self, event_id: str) -> MemoryEvent | None:
        """Return a memory event by id, if present."""

        return self._store.get_event(event_id)

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        """Return persisted events, optionally filtered by trace id."""

        return self._store.list_events(trace_id)

    def save_trace(self, trace: TaskTrace) -> None:
        """Persist or replace a task trace in memory for interface compatibility."""

        self._store.save_trace(trace)

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        """Return an in-memory task trace by id, if present."""

        return self._store.get_trace(trace_id)

    def list_traces(self) -> tuple[TaskTrace, ...]:
        """Return in-memory task traces."""

        return self._store.list_traces()

    def close(self) -> None:
        """Release backend resources."""

        return None

    def _append(self, record: dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, sort_keys=True))
            file.write("\n")

    def _replay(self) -> None:
        with self.path.open(encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("record_type") == "memory_event":
                    self._store.save_event(memory_event_from_dict(record["payload"]))
