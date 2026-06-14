from memory_aware_ros2_agent.models import RecallQuery
from memory_aware_ros2_agent.recall_engine import RecallQueryPlan, plan_recall_query


def _query(**filters: object) -> RecallQuery:
    return RecallQuery(
        query_id="query-001",
        query_text="dock",
        requested_at="2026-06-14T10:00:00Z",
        trace_id="trace-001",
        limit=3,
        filters=filters,
    )


def test_plan_recall_query_detects_filters() -> None:
    plan = plan_recall_query(
        _query(
            event_types=("task.failed",),
            started_at="2026-06-14T10:00:00Z",
            metadata={"zone": "dock"},
            source_node_ids=("node-a",),
        )
    )

    assert plan.filters == (
        "trace",
        "event_type",
        "time_window",
        "metadata",
        "source_node",
    )
    assert plan.limit == 3


def test_plan_recall_query_defaults_scorers() -> None:
    assert plan_recall_query(_query()).scorers == ("recency", "frequency")


def test_plan_recall_query_uses_requested_scorers() -> None:
    plan = plan_recall_query(_query(scorers=("exact", "recency")))

    assert plan == RecallQueryPlan(
        filters=("trace",),
        scorers=("exact", "recency"),
        limit=3,
    )
