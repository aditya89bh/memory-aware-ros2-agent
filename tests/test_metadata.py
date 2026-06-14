from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 compatibility.
    import tomli as tomllib

from memory_aware_ros2_agent import PACKAGE_NAME, __version__


def test_package_metadata_matches_pyproject() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]

    assert project["name"] == PACKAGE_NAME
    assert project["version"] == __version__
    assert project["requires-python"] == ">=3.10"
