"""Persistence backend registry."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from memory_aware_ros2_agent.event_log_store import EventLogStore
from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.json_file_store import JsonFileStore
from memory_aware_ros2_agent.persistence import MemoryStore
from memory_aware_ros2_agent.persistence_errors import BackendConfigurationError
from memory_aware_ros2_agent.sqlite_store import SQLiteStore

BackendFactory = Callable[[str | Path | None], MemoryStore]


class BackendRegistry:
    """Registry for constructing persistence backends by name."""

    def __init__(self) -> None:
        self._factories: dict[str, BackendFactory] = {}

    def register(self, name: str, factory: BackendFactory) -> None:
        """Register a backend factory."""

        self._factories[name] = factory

    def create(self, name: str, path: str | Path | None = None) -> MemoryStore:
        """Create a backend by name."""

        try:
            factory = self._factories[name]
        except KeyError as exc:
            msg = f"Unknown persistence backend: {name}"
            raise BackendConfigurationError(msg) from exc
        return factory(path)

    def names(self) -> tuple[str, ...]:
        """Return registered backend names."""

        return tuple(sorted(self._factories))


def default_backend_registry() -> BackendRegistry:
    """Create the default backend registry."""

    registry = BackendRegistry()
    registry.register("memory", lambda _path: InMemoryStore())
    registry.register("json", _require_path(JsonFileStore))
    registry.register("sqlite", _require_path(SQLiteStore))
    registry.register("event_log", _require_path(EventLogStore))
    return registry


def _require_path(
    store_type: type[JsonFileStore] | type[SQLiteStore] | type[EventLogStore],
) -> BackendFactory:
    def create(path: str | Path | None) -> MemoryStore:
        if path is None:
            msg = f"{store_type.__name__} requires a path"
            raise BackendConfigurationError(msg)
        return store_type(path)

    return create
