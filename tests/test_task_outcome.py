from memory_aware_ros2_agent.models import TaskOutcome


def test_task_outcome_stores_completion_fields() -> None:
    outcome = TaskOutcome(
        trace_id="trace-001",
        status="succeeded",
        completed_at="2026-06-13T05:10:00Z",
        metrics={"attempts": 1},
    )

    assert outcome.trace_id == "trace-001"
    assert outcome.status == "succeeded"
    assert outcome.completed_at == "2026-06-13T05:10:00Z"
    assert outcome.reason is None
    assert outcome.metrics == {"attempts": 1}


def test_task_outcome_accepts_failure_reason() -> None:
    outcome = TaskOutcome(
        trace_id="trace-002",
        status="failed",
        completed_at="2026-06-13T05:12:00Z",
        reason="Object pose confidence was too low.",
    )

    assert outcome.status == "failed"
    assert outcome.reason == "Object pose confidence was too low."
    assert outcome.metrics == {}
