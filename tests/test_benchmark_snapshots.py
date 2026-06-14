import json
from pathlib import Path
from typing import Any


def test_performance_snapshot_schema_is_valid() -> None:
    snapshot = _load_snapshot()

    assert snapshot["schema_version"] == 1
    assert {benchmark["name"] for benchmark in snapshot["benchmarks"]} == {
        "exact_match_recall",
        "load_fixture_creation",
    }


def test_performance_snapshot_thresholds_are_positive() -> None:
    snapshot = _load_snapshot()

    for benchmark in snapshot["benchmarks"]:
        assert benchmark["item_count"] > 0
        assert benchmark["max_elapsed_seconds"] > 0.0


def _load_snapshot() -> dict[str, Any]:
    path = Path("benchmarks/performance_snapshot.json")
    return json.loads(path.read_text(encoding="utf-8"))
