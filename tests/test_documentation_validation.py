from pathlib import Path


def test_required_production_documents_exist() -> None:
    required_paths = (
        Path("README.md"),
        Path("SECURITY.md"),
        Path("docs/trace_intelligence.md"),
        Path("docs/phase6_summary.md"),
    )

    for path in required_paths:
        assert path.exists()
        assert path.read_text(encoding="utf-8").strip()


def test_readme_links_phase_documentation() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/ros2_usage.md" in readme
    assert "docs/persistence.md" in readme
    assert "docs/recall_engine.md" in readme
    assert "docs/trace_intelligence.md" in readme
