"""Backup utilities for persistence artifacts."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BackupRecord:
    """A completed persistence backup."""

    source_path: Path
    backup_path: Path


def create_backup(
    source_path: str | Path,
    backup_directory: str | Path,
    label: str = "latest",
) -> BackupRecord:
    """Copy a persistence artifact into a backup directory."""

    source = Path(source_path)
    if not source.exists():
        msg = f"Cannot back up missing persistence artifact: {source}"
        raise FileNotFoundError(msg)
    backup_dir = Path(backup_directory)
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"{source.name}.{label}.bak"
    shutil.copy2(source, backup_path)
    return BackupRecord(source_path=source, backup_path=backup_path)
