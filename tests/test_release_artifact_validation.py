from pathlib import Path

from memory_aware_ros2_agent.release_validation import validate_release_artifacts


def test_validate_release_artifacts_accepts_wheel_and_sdist(tmp_path: Path) -> None:
    wheel = tmp_path / "memory_aware_ros2_agent-0.1.0-py3-none-any.whl"
    sdist = tmp_path / "memory_aware_ros2_agent-0.1.0.tar.gz"
    wheel.write_bytes(b"wheel")
    sdist.write_bytes(b"sdist")

    report = validate_release_artifacts(tmp_path)

    assert report.is_valid
    assert report.wheel_count == 1
    assert report.sdist_count == 1
    assert set(report.hashes) == {wheel.name, sdist.name}


def test_validate_release_artifacts_rejects_missing_sdist(tmp_path: Path) -> None:
    (tmp_path / "memory_aware_ros2_agent-0.1.0-py3-none-any.whl").write_bytes(
        b"wheel"
    )

    report = validate_release_artifacts(tmp_path)

    assert not report.is_valid
    assert report.wheel_count == 1
    assert report.sdist_count == 0
