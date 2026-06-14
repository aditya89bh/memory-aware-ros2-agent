from pathlib import Path

import pytest

from memory_aware_ros2_agent.backup import create_backup


def test_create_backup_copies_source_file(tmp_path: Path) -> None:
    source = tmp_path / "memory.json"
    source.write_text('{"events": {}}', encoding="utf-8")

    record = create_backup(source, tmp_path / "backups", label="phase4")

    assert record.source_path == source
    assert record.backup_path.name == "memory.json.phase4.bak"
    assert record.backup_path.read_text(encoding="utf-8") == '{"events": {}}'


def test_create_backup_rejects_missing_source(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        create_backup(tmp_path / "missing.json", tmp_path / "backups")
