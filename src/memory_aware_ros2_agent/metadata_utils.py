"""Helpers for combining event metadata."""

from __future__ import annotations

from memory_aware_ros2_agent.models import EventMetadata


def merge_tags(*tag_groups: tuple[str, ...]) -> tuple[str, ...]:
    """Merge tag tuples while preserving first-seen order."""

    merged: list[str] = []
    seen: set[str] = set()
    for tags in tag_groups:
        for tag in tags:
            if tag not in seen:
                merged.append(tag)
                seen.add(tag)
    return tuple(merged)


def merge_event_metadata(base: EventMetadata, overlay: EventMetadata) -> EventMetadata:
    """Merge metadata, letting the overlay represent the latest source context."""

    return EventMetadata(
        source_node_id=overlay.source_node_id,
        created_at=overlay.created_at,
        tags=merge_tags(base.tags, overlay.tags),
        priority=max(base.priority, overlay.priority),
    )
