from pathlib import Path


def test_readme_links_persistence_docs() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/persistence.md" in readme


def test_persistence_docs_describe_supported_backends() -> None:
    docs = Path("docs/persistence.md").read_text(encoding="utf-8")

    for backend in ("memory", "json", "sqlite", "event_log"):
        assert backend in docs
    assert "Retention" in docs
    assert "migration" in docs.lower()
