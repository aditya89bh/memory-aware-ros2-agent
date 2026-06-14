"""Migration helpers for persistence metadata."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from dataclasses import dataclass

MigrationAction = Callable[[sqlite3.Connection], None]


@dataclass(frozen=True)
class MigrationStep:
    """One SQLite schema migration step."""

    version: int
    action: MigrationAction


def get_schema_version(connection: sqlite3.Connection) -> int:
    """Return the current schema version from metadata."""

    row = connection.execute(
        "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
    ).fetchone()
    if row is None:
        return 0
    return int(row[0])


def set_schema_version(connection: sqlite3.Connection, version: int) -> None:
    """Persist the current schema version."""

    connection.execute(
        """
        INSERT OR REPLACE INTO schema_metadata (key, value)
        VALUES ('schema_version', ?)
        """,
        (str(version),),
    )
    connection.commit()


def apply_migrations(
    connection: sqlite3.Connection,
    migrations: tuple[MigrationStep, ...],
) -> tuple[int, ...]:
    """Apply migrations newer than the current schema version."""

    current_version = get_schema_version(connection)
    applied: list[int] = []
    for migration in sorted(migrations, key=lambda step: step.version):
        if migration.version <= current_version:
            continue
        migration.action(connection)
        set_schema_version(connection, migration.version)
        applied.append(migration.version)
        current_version = migration.version
    return tuple(applied)
