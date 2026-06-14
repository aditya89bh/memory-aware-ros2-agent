"""SQLite persistence backend."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from memory_aware_ros2_agent.models import MemoryEvent, RecallResult, TaskTrace
from memory_aware_ros2_agent.serialization import (
    memory_event_from_dict,
    model_to_dict,
    recall_result_from_dict,
    task_trace_from_dict,
)
from memory_aware_ros2_agent.sqlite_schema import (
    initialize_sqlite_schema,
)
from memory_aware_ros2_agent.sqlite_schema import (
    sqlite_tables as _sqlite_tables,
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

    def delete_event(self, event_id: str) -> None:
        """Delete a memory event by id if present."""

        self.connection.execute(
            "DELETE FROM memory_events WHERE event_id = ?",
            (event_id,),
        )
        self.connection.commit()

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

    def delete_trace(self, trace_id: str) -> None:
        """Delete a task trace by id if present."""

        self.connection.execute(
            "DELETE FROM task_traces WHERE trace_id = ?",
            (trace_id,),
        )
        self.connection.commit()

    def save_recall_result(self, result: RecallResult) -> None:
        """Persist or replace a recall result."""

        self.connection.execute(
            """
            INSERT OR REPLACE INTO recall_results
              (query_id, generated_at, payload_json)
            VALUES (?, ?, ?)
            """,
            (
                result.query_id,
                result.generated_at,
                json.dumps(model_to_dict(result), sort_keys=True),
            ),
        )
        self.connection.commit()

    def get_recall_result(self, query_id: str) -> RecallResult | None:
        """Return a recall result by query id, if present."""

        row = self.connection.execute(
            "SELECT payload_json FROM recall_results WHERE query_id = ?",
            (query_id,),
        ).fetchone()
        if row is None:
            return None
        return recall_result_from_dict(json.loads(str(row[0])))

    def list_recall_results(self) -> tuple[RecallResult, ...]:
        """Return persisted recall results."""

        rows = self.connection.execute(
            "SELECT payload_json FROM recall_results ORDER BY rowid"
        ).fetchall()
        return tuple(recall_result_from_dict(json.loads(str(row[0]))) for row in rows)

    def delete_recall_result(self, query_id: str) -> None:
        """Delete a recall result by query id if present."""

        self.connection.execute(
            "DELETE FROM recall_results WHERE query_id = ?",
            (query_id,),
        )
        self.connection.commit()

    def close(self) -> None:
        """Release backend resources."""

        self.connection.close()

    def _initialize_schema(self) -> None:
        initialize_sqlite_schema(self.connection)


def sqlite_tables(store: SQLiteStore) -> tuple[str, ...]:
    """Return user-created SQLite table names for tests and diagnostics."""

    return _sqlite_tables(store.connection)
