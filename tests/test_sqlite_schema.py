import sqlite3

from memory_aware_ros2_agent.sqlite_schema import (
    SCHEMA_VERSION,
    initialize_sqlite_schema,
    sqlite_indexes,
    sqlite_tables,
)


def test_initialize_sqlite_schema_creates_expected_tables() -> None:
    connection = sqlite3.connect(":memory:")

    initialize_sqlite_schema(connection)

    assert sqlite_tables(connection) == (
        "memory_events",
        "recall_results",
        "schema_metadata",
        "task_traces",
    )


def test_initialize_sqlite_schema_records_schema_version() -> None:
    connection = sqlite3.connect(":memory:")

    initialize_sqlite_schema(connection)
    row = connection.execute(
        "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
    ).fetchone()

    assert row == (str(SCHEMA_VERSION),)


def test_initialize_sqlite_schema_creates_lookup_indexes() -> None:
    connection = sqlite3.connect(":memory:")

    initialize_sqlite_schema(connection)

    assert sqlite_indexes(connection) == (
        "idx_memory_events_timestamp",
        "idx_memory_events_trace_id",
        "idx_recall_results_generated_at",
        "idx_task_traces_started_at",
    )
