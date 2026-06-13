from memory_aware_ros2_agent.models import EventMetadata


def test_event_metadata_stores_source_context() -> None:
    metadata = EventMetadata(
        source_node_id="planner-node",
        created_at="2026-06-13T05:00:00Z",
        tags=("planning", "pick"),
        priority=2,
    )

    assert metadata.source_node_id == "planner-node"
    assert metadata.created_at == "2026-06-13T05:00:00Z"
    assert metadata.tags == ("planning", "pick")
    assert metadata.priority == 2


def test_event_metadata_defaults_optional_fields() -> None:
    metadata = EventMetadata(
        source_node_id="memory-node",
        created_at="2026-06-13T05:00:00Z",
    )

    assert metadata.tags == ()
    assert metadata.priority == 0
