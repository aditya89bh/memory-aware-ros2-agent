from memory_aware_ros2_agent.factories import create_memory_event, create_recall_result
from memory_aware_ros2_agent.models import EventType


def test_create_recall_result_uses_generated_timestamp() -> None:
    result = create_recall_result(query_id="query-001")

    assert result.query_id == "query-001"
    assert result.events == ()
    assert result.scores == ()
    assert result.generated_at is not None
    assert result.generated_at.endswith("Z")


def test_create_recall_result_accepts_events_and_scores() -> None:
    event = create_memory_event(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_FAILED,
        timestamp="2026-06-13T05:05:00Z",
        summary="Grasp failed.",
    )
    result = create_recall_result(
        query_id="query-001",
        events=(event,),
        scores=(0.95,),
        generated_at="2026-06-13T05:10:00Z",
    )

    assert result.events == (event,)
    assert result.scores == (0.95,)
    assert result.generated_at == "2026-06-13T05:10:00Z"
