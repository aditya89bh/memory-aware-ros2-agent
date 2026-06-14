"""Restore utilities for persistence artifacts."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RestoreRecord:
    """A completed persistence restore."""

    backup_path: Path
    target_path: Path


def restore_backup(
    backup_path: str | Path,
    target_path: str | Path,
    *,
    overwrite: bool = False,
) -> RestoreRecord:
    """Restore a backup artifact to a target path."""

    backup = Path(backup_path)
    if not backup.exists():
        msg = f"Cannot restore missing backup artifact: {backup}"
        raise FileNotFoundError(msg)
    target = Path(target_path)
    if target.exists() and not overwrite:
        msg = f"Refusing to overwrite existing persistence artifact: {target}"
        raise FileExistsError(msg)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup, target)
    return RestoreRecord(backup_path=backup, target_path=target)
