import subprocess
import sys
import venv
from importlib.metadata import version
from pathlib import Path

import pytest


def _setuptools_supports_local_build() -> bool:
    major_version = int(version("setuptools").split(".", maxsplit=1)[0])
    return major_version >= 68


def test_built_wheel_installs_and_imports(tmp_path: Path) -> None:
    if not _setuptools_supports_local_build():
        pytest.skip("local setuptools does not satisfy build-system.requires")

    dist_dir = tmp_path / "dist"
    venv_dir = tmp_path / "venv"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--no-isolation",
            "--outdir",
            str(dist_dir),
        ],
        check=True,
    )
    wheels = tuple(dist_dir.glob("memory_aware_ros2_agent-*.whl"))
    assert len(wheels) == 1

    venv.EnvBuilder(with_pip=True).create(venv_dir)
    python = venv_dir / "bin" / "python"
    subprocess.run(
        [str(python), "-m", "pip", "install", "--no-deps", str(wheels[0])],
        check=True,
    )
    result = subprocess.run(
        [
            str(python),
            "-c",
            "import memory_aware_ros2_agent as pkg; print(pkg.PACKAGE_NAME)",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "memory-aware-ros2-agent"
