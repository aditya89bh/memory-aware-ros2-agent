import sqlite3

from memory_aware_ros2_agent.migrations import (
    MigrationStep,
    apply_migrations,
    get_schema_version,
    set_schema_version,
)
from memory_aware_ros2_agent.sqlite_schema import initialize_sqlite_schema


def test_schema_version_defaults_from_initialized_schema() -> None:
    connection = sqlite3.connect(":memory:")
    initialize_sqlite_schema(connection)

    assert get_schema_version(connection) == 1


def test_set_schema_version_updates_metadata() -> None:
    connection = sqlite3.connect(":memory:")
    initialize_sqlite_schema(connection)

    set_schema_version(connection, 2)

    assert get_schema_version(connection) == 2


def test_apply_migrations_runs_newer_steps_in_order() -> None:
    connection = sqlite3.connect(":memory:")
    initialize_sqlite_schema(connection)
    applied_names: list[str] = []

    def first(connection: sqlite3.Connection) -> None:
        connection.execute("CREATE TABLE first_migration (id TEXT)")
        applied_names.append("first")

    def second(connection: sqlite3.Connection) -> None:
        connection.execute("CREATE TABLE second_migration (id TEXT)")
        applied_names.append("second")

    applied_versions = apply_migrations(
        connection,
        (
            MigrationStep(version=3, action=second),
            MigrationStep(version=2, action=first),
        ),
    )

    assert applied_versions == (2, 3)
    assert applied_names == ["first", "second"]
    assert get_schema_version(connection) == 3


def test_apply_migrations_skips_old_versions() -> None:
    connection = sqlite3.connect(":memory:")
    initialize_sqlite_schema(connection)
    set_schema_version(connection, 3)

    applied_versions = apply_migrations(
        connection,
        (MigrationStep(version=2, action=lambda _connection: None),),
    )

    assert applied_versions == ()
    assert get_schema_version(connection) == 3
