"""SQLite persistence backend."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.models import MemoryEvent, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
    task_trace_from_dict,
)


class SQLiteStore:
    """MemoryStore implementation backed by SQLite."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def save_event(self, event: MemoryEvent) -> None:
        """Persist or replace a memory event."""

        self.connection.execute(
            """
            INSERT OR REPLACE INTO memory_events
              (event_id, trace_id, event_type, timestamp, payload_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                event.event_id,
                event.trace_id,
                event.event_type.value,
                event.timestamp,
                json.dumps(model_to_dict(event), sort_keys=True),
            ),
        )
        self.connection.commit()

    def get_event(self, event_id: str) -> MemoryEvent | None:
        """Return a memory event by id, if present."""

        row = self.connection.execute(
            "SELECT payload_json FROM memory_events WHERE event_id = ?",
            (event_id,),
        ).fetchone()
        if row is None:
            return None
        return memory_event_from_dict(json.loads(str(row[0])))

    def list_events(self, trace_id: str | None = None) -> tuple[MemoryEvent, ...]:
        """Return persisted events, optionally filtered by trace id."""

        if trace_id is None:
            rows = self.connection.execute(
                "SELECT payload_json FROM memory_events ORDER BY rowid"
            ).fetchall()
        else:
            rows = self.connection.execute(
                """
                SELECT payload_json FROM memory_events
                WHERE trace_id = ?
                ORDER BY rowid
                """,
                (trace_id,),
            ).fetchall()
        return tuple(memory_event_from_dict(json.loads(str(row[0]))) for row in rows)

    def save_trace(self, trace: TaskTrace) -> None:
        """Persist or replace a task trace."""

        self.connection.execute(
            """
            INSERT OR REPLACE INTO task_traces
              (trace_id, task_name, started_at, payload_json)
            VALUES (?, ?, ?, ?)
            """,
            (
                trace.trace_id,
                trace.task_name,
                trace.started_at,
                json.dumps(model_to_dict(trace), sort_keys=True),
            ),
        )
        self.connection.commit()

    def get_trace(self, trace_id: str) -> TaskTrace | None:
        """Return a task trace by id, if present."""

        row = self.connection.execute(
            "SELECT payload_json FROM task_traces WHERE trace_id = ?",
            (trace_id,),
        ).fetchone()
        if row is None:
            return None
        return task_trace_from_dict(json.loads(str(row[0])))

    def list_traces(self) -> tuple[TaskTrace, ...]:
        """Return persisted task traces."""

        rows = self.connection.execute(
            "SELECT payload_json FROM task_traces ORDER BY rowid"
        ).fetchall()
        return tuple(task_trace_from_dict(json.loads(str(row[0]))) for row in rows)

    def close(self) -> None:
        """Release backend resources."""

        self.connection.close()

    def _initialize_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS memory_events (
                event_id TEXT PRIMARY KEY,
                trace_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS task_traces (
                trace_id TEXT PRIMARY KEY,
                task_name TEXT NOT NULL,
                started_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            """
        )
        self.connection.commit()


def sqlite_tables(store: SQLiteStore) -> tuple[str, ...]:
    """Return user-created SQLite table names for tests and diagnostics."""

    rows: list[tuple[Any, ...]] = store.connection.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()
    return tuple(str(row[0]) for row in rows)
