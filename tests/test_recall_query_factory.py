from memory_aware_ros2_agent.factories import create_recall_query


def test_create_recall_query_uses_generated_defaults() -> None:
    query = create_recall_query(query_text="Find prior failures.")

    assert query.query_id.startswith("query-")
    assert query.query_text == "Find prior failures."
    assert query.requested_at.endswith("Z")
    assert query.trace_id is None
    assert query.limit == 5
    assert query.filters == {}


def test_create_recall_query_accepts_explicit_values() -> None:
    query = create_recall_query(
        query_id="query-001",
        query_text="Find grasp attempts.",
        requested_at="2026-06-13T05:10:00Z",
        trace_id="trace-001",
        limit=3,
        filters={"event_type": "task.failed"},
    )

    assert query.query_id == "query-001"
    assert query.requested_at == "2026-06-13T05:10:00Z"
    assert query.trace_id == "trace-001"
    assert query.limit == 3
    assert query.filters == {"event_type": "task.failed"}
