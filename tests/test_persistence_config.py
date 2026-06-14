import json
from pathlib import Path

import pytest

from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.json_file_store import JsonFileStore
from memory_aware_ros2_agent.persistence_config import (
    PersistenceConfig,
    create_store_from_config,
    load_persistence_config,
    persistence_config_from_dict,
)


def test_persistence_config_defaults_to_memory_backend() -> None:
    config = persistence_config_from_dict({})

    assert config == PersistenceConfig()
    assert isinstance(create_store_from_config(config), InMemoryStore)


def test_load_persistence_config_reads_json_file(tmp_path: Path) -> None:
    path = tmp_path / "persistence.json"
    path.write_text(
        json.dumps({"backend": "json", "path": str(tmp_path / "memory.json")}),
        encoding="utf-8",
    )

    config = load_persistence_config(path)

    assert config.backend == "json"
    assert config.path == str(tmp_path / "memory.json")


def test_create_store_from_config_uses_registry(tmp_path: Path) -> None:
    config = PersistenceConfig(backend="json", path=str(tmp_path / "memory.json"))

    assert isinstance(create_store_from_config(config), JsonFileStore)


def test_load_persistence_config_rejects_non_object_json(tmp_path: Path) -> None:
    path = tmp_path / "persistence.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="JSON object"):
        load_persistence_config(path)
