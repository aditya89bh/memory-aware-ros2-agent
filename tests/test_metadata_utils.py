from memory_aware_ros2_agent.metadata_utils import merge_event_metadata, merge_tags
from memory_aware_ros2_agent.models import EventMetadata


def test_merge_tags_preserves_first_seen_order() -> None:
    assert merge_tags(("pick", "vision"), ("vision", "retry")) == (
        "pick",
        "vision",
        "retry",
    )


def test_merge_event_metadata_combines_tags_and_priority() -> None:
    base = EventMetadata(
        source_node_id="planner",
        created_at="2026-06-13T05:00:00Z",
        tags=("pick",),
        priority=1,
    )
    overlay = EventMetadata(
        source_node_id="recovery",
        created_at="2026-06-13T05:01:00Z",
        tags=("pick", "retry"),
        priority=3,
    )

    merged = merge_event_metadata(base, overlay)

    assert merged.source_node_id == "recovery"
    assert merged.created_at == "2026-06-13T05:01:00Z"
    assert merged.tags == ("pick", "retry")
    assert merged.priority == 3
