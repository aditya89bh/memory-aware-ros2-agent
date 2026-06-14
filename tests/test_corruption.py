import sqlite3
from pathlib import Path

from memory_aware_ros2_agent.corruption import (
    check_event_log,
    check_json_file,
    check_sqlite_database,
)


def test_check_json_file_reports_valid_json(tmp_path: Path) -> None:
    path = tmp_path / "memory.json"
    path.write_text('{"events": {}}', encoding="utf-8")

    assert check_json_file(path).is_corrupt is False


def test_check_json_file_reports_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "memory.json"
    path.write_text("{", encoding="utf-8")

    report = check_json_file(path)

    assert report.is_corrupt is True
    assert report.reason is not None


def test_check_event_log_reports_invalid_json_line(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    path.write_text('{"record_type": "memory_event"}\n{\n', encoding="utf-8")

    assert check_event_log(path).is_corrupt is True


def test_check_sqlite_database_runs_integrity_check(tmp_path: Path) -> None:
    path = tmp_path / "memory.db"
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE records (id TEXT PRIMARY KEY)")
    connection.close()

    assert check_sqlite_database(path).is_corrupt is False
