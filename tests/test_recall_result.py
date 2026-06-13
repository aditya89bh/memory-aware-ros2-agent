from memory_aware_ros2_agent.models import EventType, MemoryEvent, RecallResult


def test_recall_result_defaults_to_empty_events() -> None:
    result = RecallResult(query_id="query-001")

    assert result.query_id == "query-001"
    assert result.events == ()
    assert result.scores == ()
    assert result.generated_at is None


def test_recall_result_stores_events_and_scores() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_FAILED,
        timestamp="2026-06-13T05:03:00Z",
        summary="Grasp attempt failed.",
    )
    result = RecallResult(
        query_id="query-001",
        events=(event,),
        scores=(0.87,),
        generated_at="2026-06-13T05:16:00Z",
    )

    assert result.events == (event,)
    assert result.scores == (0.87,)
    assert result.generated_at == "2026-06-13T05:16:00Z"
