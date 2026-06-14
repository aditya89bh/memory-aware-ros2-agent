import importlib.util
from pathlib import Path
from types import ModuleType


def _load_launch_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_launch_examples_define_launch_descriptions() -> None:
    launch_files = sorted(Path("launch").glob("*.launch.py"))

    assert {path.name for path in launch_files} == {
        "memory_lifecycle.launch.py",
        "memory_pipeline.launch.py",
    }
    for path in launch_files:
        module = _load_launch_module(path)
        launch_description = module.generate_launch_description()
        assert launch_description is not None
