import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any


def _load_launch_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _launch_entities(path: str) -> list[Any]:
    module = _load_launch_module(Path(path))
    return list(module.generate_launch_description().entities)


def test_memory_pipeline_launch_includes_core_node_executables() -> None:
    entities = _launch_entities("launch/memory_pipeline.launch.py")

    executables = {entity.node_executable for entity in entities}

    assert executables == {
        "memory-recorder",
        "recall-service",
        "trace-publisher",
        "trace-subscriber",
    }


def test_memory_pipeline_launch_uses_expected_package() -> None:
    entities = _launch_entities("launch/memory_pipeline.launch.py")

    for entity in entities:
        assert entity.node_package == "memory_aware_ros2_agent"


def test_memory_lifecycle_launch_includes_lifecycle_node() -> None:
    entities = _launch_entities("launch/memory_lifecycle.launch.py")

    assert len(entities) == 1
    assert entities[0].node_executable == "memory-lifecycle"
