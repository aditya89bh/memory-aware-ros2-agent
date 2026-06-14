from memory_aware_ros2_agent.load_fixtures import (
    make_load_recall_query,
    make_load_store,
    make_load_trace,
)
from memory_aware_ros2_agent.recall_engine import ExactMatchRecallEngine


def test_make_load_trace_creates_deterministic_events() -> None:
    trace = make_load_trace(event_count=3)

    assert trace.trace_id == "trace-load"
    assert tuple(event.event_id for event in trace.events) == (
        "trace-load-event-0",
        "trace-load-event-1",
        "trace-load-event-2",
    )


def test_make_load_store_populates_recall_ready_data() -> None:
    store = make_load_store(event_count=12)
    query = make_load_recall_query(limit=5)

    result = ExactMatchRecallEngine().recall(query, store)

    assert len(store.list_events("trace-load")) == 12
    assert len(result.events) == 5
    assert result.scores == (1.0, 1.0, 1.0, 1.0, 1.0)
