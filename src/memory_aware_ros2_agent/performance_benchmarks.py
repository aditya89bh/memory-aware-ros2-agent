"""Performance benchmark automation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from memory_aware_ros2_agent.load_fixtures import (
    make_load_recall_query,
    make_load_store,
)
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


@dataclass(frozen=True)
class BenchmarkResult:
    """Measured benchmark result."""

    name: str
    item_count: int
    elapsed_seconds: float


def benchmark_load_fixture_creation(event_count: int) -> BenchmarkResult:
    """Measure load fixture store creation time."""

    started_at = perf_counter()
    make_load_store(event_count)
    return BenchmarkResult(
        name="load_fixture_creation",
        item_count=event_count,
        elapsed_seconds=perf_counter() - started_at,
    )


def benchmark_exact_match_recall(event_count: int, limit: int) -> BenchmarkResult:
    """Measure exact-match recall over load fixture data."""

    store = make_load_store(event_count)
    query = make_load_recall_query(limit=limit)
    engine = ExactMatchRecallEngine()
    started_at = perf_counter()
    result = engine.recall(query, store)
    return BenchmarkResult(
        name="exact_match_recall",
        item_count=len(result.events),
        elapsed_seconds=perf_counter() - started_at,
    )
