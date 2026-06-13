import tomllib
from pathlib import Path

from memory_aware_ros2_agent import PACKAGE_NAME, __version__


def test_package_metadata_matches_pyproject() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]

    assert PACKAGE_NAME == project["name"]
    assert __version__ == project["version"]
    assert project["requires-python"] == ">=3.10"
