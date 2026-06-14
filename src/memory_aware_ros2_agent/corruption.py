"""Corruption detection helpers for persistence files."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CorruptionReport:
    """Result of checking a persistence artifact."""

    is_corrupt: bool
    reason: str | None = None


def check_json_file(path: str | Path) -> CorruptionReport:
    """Check whether a JSON persistence file can be decoded."""

    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return CorruptionReport(is_corrupt=True, reason=str(exc))
    if not isinstance(data, dict):
        return CorruptionReport(is_corrupt=True, reason="JSON root must be an object")
    return CorruptionReport(is_corrupt=False)


def check_event_log(path: str | Path) -> CorruptionReport:
    """Check whether an append-only JSONL event log can be decoded."""

    try:
        with Path(path).open(encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    json.loads(line)
    except (OSError, json.JSONDecodeError) as exc:
        return CorruptionReport(is_corrupt=True, reason=str(exc))
    return CorruptionReport(is_corrupt=False)


def check_sqlite_database(path: str | Path) -> CorruptionReport:
    """Run SQLite integrity_check against a database."""

    try:
        connection = sqlite3.connect(Path(path))
        row = connection.execute("PRAGMA integrity_check").fetchone()
        connection.close()
    except sqlite3.DatabaseError as exc:
        return CorruptionReport(is_corrupt=True, reason=str(exc))
    if row != ("ok",):
        return CorruptionReport(is_corrupt=True, reason=str(row[0]))
    return CorruptionReport(is_corrupt=False)
