"""Persistence backend configuration loading."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from memory_aware_ros2_agent.backend_registry import default_backend_registry
from memory_aware_ros2_agent.persistence import MemoryStore
from memory_aware_ros2_agent.persistence_errors import BackendConfigurationError


@dataclass(frozen=True)
class PersistenceConfig:
    """Configuration for constructing a persistence backend."""

    backend: str = "memory"
    path: str | None = None


def persistence_config_from_dict(data: dict[str, Any]) -> PersistenceConfig:
    """Load persistence configuration from a dictionary."""

    path = data.get("path")
    return PersistenceConfig(
        backend=str(data.get("backend", "memory")),
        path=None if path is None else str(path),
    )


def load_persistence_config(path: str | Path) -> PersistenceConfig:
    """Load persistence configuration from a JSON file."""

    with Path(path).open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        msg = "Persistence config must be a JSON object"
        raise BackendConfigurationError(msg)
    return persistence_config_from_dict(data)


def create_store_from_config(config: PersistenceConfig) -> MemoryStore:
    """Create a persistence backend from configuration."""

    return default_backend_registry().create(config.backend, config.path)
