from memory_aware_ros2_agent.models import RecallQuery


def test_recall_query_stores_request_fields() -> None:
    query = RecallQuery(
        query_id="query-001",
        query_text="What happened during the last grasp attempt?",
        requested_at="2026-06-13T05:15:00Z",
        trace_id="trace-001",
    )

    assert query.query_id == "query-001"
    assert query.query_text == "What happened during the last grasp attempt?"
    assert query.requested_at == "2026-06-13T05:15:00Z"
    assert query.trace_id == "trace-001"
    assert query.limit == 5
    assert query.filters == {}


def test_recall_query_accepts_filters_and_limit() -> None:
    query = RecallQuery(
        query_id="query-002",
        query_text="Find failed events.",
        requested_at="2026-06-13T05:16:00Z",
        limit=10,
        filters={"event_type": "task.failed"},
    )

    assert query.limit == 10
    assert query.filters == {"event_type": "task.failed"}
