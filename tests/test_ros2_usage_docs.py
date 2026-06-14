from pathlib import Path


def test_ros2_usage_doc_is_linked_from_readme() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/ros2_usage.md" in readme


def test_ros2_usage_doc_mentions_core_nodes() -> None:
    usage_doc = Path("docs/ros2_usage.md").read_text(encoding="utf-8")

    for executable in (
        "memory-recorder",
        "recall-service",
        "trace-publisher",
        "trace-subscriber",
        "memory-lifecycle",
    ):
        assert executable in usage_doc


def test_ros2_usage_doc_lists_validation_commands() -> None:
    usage_doc = Path("docs/ros2_usage.md").read_text(encoding="utf-8")

    for command in ("pytest", "ruff check .", "mypy src", "colcon build"):
        assert command in usage_doc
