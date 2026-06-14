from memory_aware_ros2_agent.in_memory_store import InMemoryStore
from memory_aware_ros2_agent.models import RecallResult
from memory_aware_ros2_agent.persistence_api import (
    load_recall_result,
    load_recall_results,
    persist_recall_result,
)


def _result(query_id: str) -> RecallResult:
    return RecallResult(query_id=query_id, generated_at="2026-06-14T10:00:00Z")


def test_persist_recall_result_saves_and_returns_result() -> None:
    store = InMemoryStore()
    result = _result("query-001")

    saved = persist_recall_result(store, result)

    assert saved == result
    assert load_recall_result(store, "query-001") == result


def test_load_recall_results_returns_all_persisted_results() -> None:
    store = InMemoryStore()
    first = _result("query-001")
    second = _result("query-002")
    persist_recall_result(store, first)
    persist_recall_result(store, second)

    assert load_recall_results(store) == (first, second)
