from pathlib import Path

import pytest

from memory_aware_ros2_agent.backend_registry import default_backend_registry
from memory_aware_ros2_agent.event_log_store import EventLogStore
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.json_file_store import JsonFileStore
from memory_aware_ros2_agent.sqlite_store import SQLiteStore


def test_default_backend_registry_lists_supported_backends() -> None:
    registry = default_backend_registry()

    assert registry.names() == ("event_log", "json", "memory", "sqlite")


def test_default_backend_registry_creates_memory_backend() -> None:
    registry = default_backend_registry()

    assert isinstance(registry.create("memory"), InMemoryStore)


def test_default_backend_registry_creates_path_backends(tmp_path: Path) -> None:
    registry = default_backend_registry()

    assert isinstance(registry.create("json", tmp_path / "memory.json"), JsonFileStore)
    assert isinstance(registry.create("sqlite", tmp_path / "memory.db"), SQLiteStore)
    assert isinstance(
        registry.create("event_log", tmp_path / "events.jsonl"),
        EventLogStore,
    )


def test_default_backend_registry_requires_paths_for_file_backends() -> None:
    registry = default_backend_registry()

    with pytest.raises(ValueError, match="requires a path"):
        registry.create("json")


def test_default_backend_registry_rejects_unknown_backend() -> None:
    registry = default_backend_registry()

    with pytest.raises(ValueError, match="Unknown persistence backend"):
        registry.create("unknown")
