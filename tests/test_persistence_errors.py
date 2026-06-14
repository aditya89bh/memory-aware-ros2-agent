import pytest

from memory_aware_ros2_agent.backend_registry import default_backend_registry
from memory_aware_ros2_agent.persistence_config import load_persistence_config
from memory_aware_ros2_agent.persistence_errors import (
    BackendConfigurationError,
    PersistenceBackupError,
    PersistenceCorruptionError,
    PersistenceError,
)


def test_persistence_error_types_share_base_class() -> None:
    assert issubclass(BackendConfigurationError, PersistenceError)
    assert issubclass(PersistenceCorruptionError, PersistenceError)
    assert issubclass(PersistenceBackupError, PersistenceError)


def test_backend_registry_raises_configuration_error_for_unknown_backend() -> None:
    registry = default_backend_registry()

    with pytest.raises(BackendConfigurationError):
        registry.create("unknown")


def test_config_loader_raises_configuration_error_for_non_object_json(tmp_path) -> None:
    path = tmp_path / "persistence.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(BackendConfigurationError):
        load_persistence_config(path)
