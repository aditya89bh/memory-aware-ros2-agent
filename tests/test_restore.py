from pathlib import Path

import pytest

from memory_aware_ros2_agent.restore import restore_backup


def test_restore_backup_copies_backup_to_target(tmp_path: Path) -> None:
    backup = tmp_path / "memory.json.latest.bak"
    backup.write_text('{"events": {}}', encoding="utf-8")

    record = restore_backup(backup, tmp_path / "active" / "memory.json")

    assert record.backup_path == backup
    assert record.target_path.read_text(encoding="utf-8") == '{"events": {}}'


def test_restore_backup_rejects_missing_backup(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        restore_backup(tmp_path / "missing.bak", tmp_path / "memory.json")


def test_restore_backup_requires_overwrite_for_existing_target(tmp_path: Path) -> None:
    backup = tmp_path / "memory.json.latest.bak"
    target = tmp_path / "memory.json"
    backup.write_text("backup", encoding="utf-8")
    target.write_text("active", encoding="utf-8")

    with pytest.raises(FileExistsError):
        restore_backup(backup, target)

    restore_backup(backup, target, overwrite=True)

    assert target.read_text(encoding="utf-8") == "backup"
