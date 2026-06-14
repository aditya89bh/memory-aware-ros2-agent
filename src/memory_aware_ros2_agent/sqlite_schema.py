"""SQLite schema helpers for persistence backends."""

from __future__ import annotations

import sqlite3
from typing import Any

SCHEMA_VERSION = 1


def initialize_sqlite_schema(connection: sqlite3.Connection) -> None:
    """Create SQLite persistence tables if they do not already exist."""

    connection.executescript(
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

        CREATE TABLE IF NOT EXISTS recall_results (
            query_id TEXT PRIMARY KEY,
            generated_at TEXT,
            payload_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS schema_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_memory_events_trace_id
            ON memory_events(trace_id);
        CREATE INDEX IF NOT EXISTS idx_memory_events_timestamp
            ON memory_events(timestamp);
        CREATE INDEX IF NOT EXISTS idx_task_traces_started_at
            ON task_traces(started_at);
        CREATE INDEX IF NOT EXISTS idx_recall_results_generated_at
            ON recall_results(generated_at);
        """
    )
    connection.execute(
        """
        INSERT OR REPLACE INTO schema_metadata (key, value)
        VALUES ('schema_version', ?)
        """,
        (str(SCHEMA_VERSION),),
    )
    connection.commit()


def sqlite_tables(connection: sqlite3.Connection) -> tuple[str, ...]:
    """Return user-created SQLite table names."""

    rows: list[tuple[Any, ...]] = connection.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()
    return tuple(str(row[0]) for row in rows)


def sqlite_indexes(connection: sqlite3.Connection) -> tuple[str, ...]:
    """Return user-created SQLite index names."""

    rows: list[tuple[Any, ...]] = connection.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type = 'index'
          AND name NOT LIKE 'sqlite_autoindex%'
        ORDER BY name
        """
    ).fetchall()
    return tuple(str(row[0]) for row in rows)
