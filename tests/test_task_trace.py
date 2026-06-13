from memory_aware_ros2_agent.models import EventType, MemoryEvent, TaskTrace


def test_task_trace_stores_workflow_fields() -> None:
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
    )

    assert trace.trace_id == "trace-001"
    assert trace.task_name == "pick-and-place"
    assert trace.started_at == "2026-06-13T05:00:00Z"
    assert trace.ended_at is None
    assert trace.events == ()


def test_task_trace_groups_memory_events() -> None:
    event = MemoryEvent(
        event_id="event-001",
        trace_id="trace-001",
        event_type=EventType.TASK_STARTED,
        timestamp="2026-06-13T05:00:00Z",
        summary="Robot started task.",
    )
    trace = TaskTrace(
        trace_id="trace-001",
        task_name="pick-and-place",
        started_at="2026-06-13T05:00:00Z",
        events=(event,),
        ended_at="2026-06-13T05:10:00Z",
    )

    assert trace.events == (event,)
    assert trace.ended_at == "2026-06-13T05:10:00Z"
