from pathlib import Path


def test_readme_links_recall_docs() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/recall_engine.md" in readme
    assert "docs/phase5_summary.md" in readme


def test_recall_docs_cover_engine_features() -> None:
    docs = Path("docs/recall_engine.md").read_text(encoding="utf-8")

    for term in (
        "ExactMatchRecallEngine",
        "TaskBasedRecallEngine",
        "TimeWindowRecallEngine",
        "event_types",
        "Composite scoring",
        "precision/recall/F1",
    ):
        assert term in docs


def test_phase5_summary_marks_recall_complete() -> None:
    summary = Path("docs/phase5_summary.md").read_text(encoding="utf-8")

    assert "Phase 5 recall engine support is complete" in summary
    assert "Semantic embeddings and vector indexes remain out of scope" in summary
